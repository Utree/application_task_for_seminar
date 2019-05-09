import keras # Kerasをインポート
from keras.preprocessing.image import load_img, img_to_array # 画像関係のライブラリ
import numpy as np
from keras.applications import vgg19 # vgg19(学習済みのCNNネットワーク)をインポート
from keras import backend as K
from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import imsave
import time
from matplotlib import pyplot as plt
import os

# base dir
# BASE_DIR = "/home/ubuntu/workspace/project/uploaded_files/api_v1/images/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images/')

# 画像を前処理する関数
def preprocess_image(image_path, img_height, img_width):
    # 画像を指定サイズで読み込む
    img = load_img(image_path, target_size=(img_height, img_width))
    # 読み込んだ画像をnumpyのarray型に変換
    img = img_to_array(img)
    # 軸を指定して、次元を追加  [0, 1, 2] -> [[0, 1, 2]]みたいな感じ
    img = np.expand_dims(img, axis=0)
    # vgg19で利用できるように前処理をする
    img = vgg19.preprocess_input(img)
    # 前処理した結果を返す
    return img

# 画像の後処理
def deprocess_image(x):
    # ImageNetから平均ピクセル値を取り除くことにより、中心を0に設定
    # これにより、vgg19.preprocess_inputによって実行される変換が逆になる
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    # 画像を'BGR'から'RGB'に変換
    # これもvgg19.preprocess_inputの変換を逆にするための措置
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    return x

# コンテンツの損失関数を定義する関数
def content_loss(base, combination):
    return K.sum(K.square(combination - base))

# グラム行列を計算するらしい(なんだそれ？)
def gram_matrix(x):
    features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram

# スタイルの損失関数(あんまりよくわかってない)
def style_loss(style, combination, img_height, img_width):
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = img_height * img_width
    return K.sum(K.square(S - C)) / (4. * (channels ** 2) * (size ** 2))

def total_variation_loss(x, img_height, img_width):
    a = K.square(x[:, :img_height - 1, :img_width - 1, :] - x[:, 1:, :img_width - 1, :])
    b = K.square(x[:, :img_height - 1, :img_width - 1, :] - x[:, :img_height - 1, 1:, :])
    return K.sum(K.pow(a + b, 1.25))

# このクラスは、損失関数の値と勾配の値を２つのメソッド呼び出しを通じて取得できるように
# fetch_loss_and_gradsをラッピングする。この２つのメソッド呼び出しは、
# ここで使用するSciPyのオプティマイザによって要求される
class Evaluator(object):
    def __init__(self, img_height, img_width, fetch_loss_and_grads):
        self.loss_value = None
        self.grads_values = None
        self.img_height = img_height
        self.img_width = img_width
        self.fetch_loss_and_grads = fetch_loss_and_grads

    def loss(self, x):
        assert self.loss_value is None
        x = x.reshape((1, self.img_height, self.img_width, 3))
        outs = self.fetch_loss_and_grads([x])
        loss_value = outs[0]
        grad_values = outs[1].flatten().astype('float64')
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value

    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values

def style_transfer(original_image, style_image, file_name):
    # 変換前の画像へのパス
    target_image_path = os.path.join(BASE_DIR, original_image)
    # スタイル画像へのパス
    style_reference_image_path = os.path.join(BASE_DIR, style_image)
    # スタイル画像のサイズを取得
    width, height = load_img(target_image_path).size
    # 大きさを縦400pxを基準に縮小
    img_height = 400
    img_width = int(width * img_height / height)

    # ターゲット画像を保持するプレースホルダ(データが格納される入れ物)
    target_image = K.constant(preprocess_image(target_image_path, img_height, img_width))
    # スタイル画像を保持するプレースホルダ(データが格納される入れ物)
    style_reference_image = K.constant(preprocess_image(style_reference_image_path, img_height, img_width))
    # 生成された画像を保持するプレースホルダ(データが格納される入れ物)
    combination_image = K.placeholder((1, img_height, img_width, 3))
    # 3つの画像を１つのバッチにまとめる
    input_tensor = K.concatenate([target_image, style_reference_image, combination_image], axis=0)
    # 3つの画像からなるバッチを入力として使用するVGG19モデルを構築
    # このモデルには、学習済みのImageNetの重みが読み込まれる
    model = vgg19.VGG19(input_tensor=input_tensor, weights='imagenet', include_top=False)
    print('Model loaded.')

    # 層の名前を活性化テンソルにマッピングするディクショナリ
    outputs_dict = dict([(layer.name, layer.output) for layer in model.layers])
    content_layer = 'block5_conv2' # コンテンツの損失関数に使用する層の名前
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']
    # 損失関数の加重平均の重み
    total_variation_weight = 1e-4
    style_weight = 1.
    content_weight = 0.025
    # すべてのコンポーネントをこのスカラー変数に追加することで、損失関数を定義
    loss = K.variable(0.)
    # コンテンツの損失関数を追加
    layer_features = outputs_dict[content_layer]
    target_image_features = layer_features[0, :, :, :]
    combination_features = layer_features[2, :, :, :]
    loss = loss + (content_weight * content_loss(target_image_features, combination_features))

    # 各ターゲット層のスタイルの損失関数を追加
    for layer_name in style_layers:
        layer_features = outputs_dict[layer_name]
        style_reference_features = layer_features[1, :, :, :]
        combination_features = layer_features[2, :, :, :]
        sl = style_loss(style_reference_features, combination_features, img_height, img_width)
        loss = loss + ((style_weight / len(style_layers)) * sl)

    # 全変動損失関数を追加
    loss = loss + (total_variation_weight * total_variation_loss(combination_image, img_height, img_width))
    # 損失関数をもとに、生成された画像の勾配を取得
    grads = K.gradients(loss, combination_image)[0]
    # 現在の損失関数の値と勾配の値を取得する関数
    fetch_loss_and_grads = K.function([combination_image], [loss, grads])

    evaluator = Evaluator(img_height, img_width, fetch_loss_and_grads)

    result_prefix = 'style_transfer_result'
    iterations = 1
    # 初期状態: ターゲット画像
    x = preprocess_image(target_image_path, img_height, img_width)
    # 画像を平坦化: scipy.optimize.fmin_l_bfgs_bは１次元ベクトルしか処理しない
    x = x.flatten()
    for i in range(iterations):
        print('Start of iteration', i)
        start_time = time.time()
        # ニューラルスタイル変換の損失関数を最小化するために、
        # 生成された画像のピクセルにわたってL-BFGS最適化を実行
        # 損失関数を計算する関数と勾配を計算する関数を２つの別々の引数として
        # 渡さなければならないことに注意
        x, min_val, info = fmin_l_bfgs_b(evaluator.loss, x, fprime=evaluator.grads, maxfun=20)
        print('Current loss value: ', min_val)
        # この時点の生成された画像を保存
        img = x.copy().reshape((img_height, img_width, 3))
        img = deprocess_image(img)
        imsave(os.path.join(BASE_DIR, file_name), img)
        end_time = time.time()
        print('Image saved')
        print('Iteration %d completed in %ds' % (i, end_time - start_time))

    # 元の画像を削除
    os.remove(os.path.join(BASE_DIR, original_image))
    os.remove(os.path.join(BASE_DIR, style_image))
