import cv2
import os

# base dir
# BASE_DIR = "/home/ubuntu/workspace/project/uploaded_files/api_v1/images/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images/')

def Gray(image_name):
    # 画像を読み込む
    img = cv2.imread(os.path.join(BASE_DIR, image_name))

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 保存
    cv2.imwrite(os.path.join(BASE_DIR, image_name), gray)
