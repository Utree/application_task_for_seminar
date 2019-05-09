import cv2
import os

# base dir
# BASE_DIR = "/home/ubuntu/workspace/project/uploaded_files/api_v1/images/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images/')

def Canny(image_name):
    # 画像を読み込む
    img = cv2.imread(os.path.join(BASE_DIR, image_name))

    # キャニー法でエッジ検出
    edge = cv2.Canny(img, 100, 200)

    # 保存
    cv2.imwrite(os.path.join(BASE_DIR, image_name), edge)
