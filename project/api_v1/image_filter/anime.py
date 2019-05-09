import cv2
import numpy as np
import os

# base dir
# BASE_DIR = "/home/ubuntu/workspace/project/uploaded_files/api_v1/images/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images/')
# 定数
K = 30

def Anime(image_name):
    print("image_name" + os.path.join(BASE_DIR, image_name))
    # 画像を読み込む
    img = cv2.imread(os.path.join(BASE_DIR, image_name))

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # ぼかしでノイズ低減
    edge = cv2.blur(gray, (3, 3))

    # Cannyアルゴリズムで輪郭抽出
    edge = cv2.Canny(edge, 50, 150, apertureSize=3)

    # 輪郭画像をRGB色空間に変換
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 次元数を1落とす(縦x横を直列化)
    Z = img.reshape((-1,3))

    # float32型に変換
    Z = np.float32(Z)

    # 基準の定義
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # K-means法で減色
    _, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # UINT8に変換
    center = np.uint8(center)

    res = center[label.flatten()]

    # 配列の次元数と入力画像と同じに戻す
    img = res.reshape((img.shape))

    # 差分を返す
    img = cv2.subtract(img, edge)

    # 保存
    cv2.imwrite(os.path.join(BASE_DIR, image_name), img)
