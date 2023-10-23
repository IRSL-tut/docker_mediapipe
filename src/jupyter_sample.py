import cv2
import numpy as np

from src.mppack import mp_hand
from src.mppack import camera_capture

cap = camera_capture.CvCapture(0)

img = cap.capture()

cap.show(img)

hands = mp_hand.MPHand(max_num_hands=1) # 手の認識モデル生成
hands.set_image(img)
res = hands.get_results()

hans
