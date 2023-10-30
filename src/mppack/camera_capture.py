import cv2
import numpy as np
import time

class CvCapture(object):
    def __init__(self, camID=0):
        self.cap = cv2.VideoCapture(camID)   # カメラのID指定
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def isOpened(self):
        return self.cap.isOpened()

    def capture(self, size=(1280, 960), flip=True, grab=True, delay=None):
        if delay is not None:
            time.sleep(delay)

        if self.cap.isOpened():
            if grab:
                self.cap.grab()
                success, img = self.cap.read()
            # カメラから画像取得
            success, img = self.cap.read()
            if not success:
                return None

            if size is not None:
                img = cv2.resize(img, size) # リサイズ
            if flip:
                img = cv2.flip(img, 1)      # 画像を左右反転

            return img

    def show(self, img, wait=10, title='IRSLCap'):
        cv2.imshow(title, img)
        key = cv2.waitKey(wait)
        return key
