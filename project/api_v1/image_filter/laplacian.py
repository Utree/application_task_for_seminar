import cv2
import os

# base dir
# BASE_DIR = "/home/ubuntu/workspace/project/uploaded_files/api_v1/images/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images/')

def Laplacian(image_name):
    # 画像を読み込む
    img = cv2.imread(os.path.join(BASE_DIR, image_name))

    # Gaussianフィルタで平滑化(ぼかす)
    img = cv2.GaussianBlur(img, (1, 1), 0)

    # Laplacianフィルタ
    lap = cv2.Laplacian(img, cv2.CV_32F)

    # 8ビット符号無し整数に変換
    edge_lap = cv2.convertScaleAbs(lap)

    # 保存
    cv2.imwrite(os.path.join(BASE_DIR, image_name), edge_lap)
