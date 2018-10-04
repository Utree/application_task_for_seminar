import cv2
import os

# base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

d
# 画像を読み込む
img = cv2.imread(os.path.join(BASE_DIR, 'static/momiji1.jpg'))

# グレースケールに変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# sobelフィルタでx方向のエッジ検出
sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
# sobelフィルタでy方向のエッジ検出
sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1)

# 8ビット符号なし整数変換
abs_sobel_x = cv2.convertScaleAbs(sobel_x)
abs_sobel_y = cv2.convertScaleAbs(sobel_y)

# 重み付き和
sobel_edge = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

cv2.imwrite(os.path.join(BASE_DIR, 'static/sobel_momiji1.jpg'), sobel_edge)
cv2.imwrite(os.path.join(BASE_DIR, 'static/sobel_momiji1.jpg'), sobel_edge)