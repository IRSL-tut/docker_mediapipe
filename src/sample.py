import colorsys
import os
import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class MPHand():
    def __init__(self, max_num_hands=1, min_detection_confidence=0.5, min_hand_presence_confidence=0.5, min_tracking_confidence=0.5):
        '''
        max_num_hands:                  (range:>0,      default:1),     検出する手の最大数
        min_detection_confidence:       (range:0.0~1.0, default:0.5),   手のひら検出モデルで成功したとみなされる手の検出の最小信頼スコア
        min_hand_presence_confidence:   (range:0.0~1.0, default:0.5),   手のランドマーク検出モデルにおける手の存在スコアの最小信頼スコア
        min_tracking_confidence:        (range:0.0~1.0, default:0.5),   ハンドトラッキングが成功したとみなされるための最小信頼スコア
        '''
        model_path = os.path.dirname(os.path.abspath(__file__)) + '/task/gesture_recognizer.task'   #'./task/gesture_recognizer.task'
        base_options = python.BaseOptions(model_asset_path=model_path)
        VisionRunningMode = vision.RunningMode
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.callback,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.results = None

        self.bone_link = [
            [0,1,2,3,4],
            [1,5,6,7,8],
            [9,10,11,12],
            [13,14,15,16],
            [0,17,18,19,20],
            [5,9,13,17],
        ]

        self.ges_time = [{'recognize':float(time.time()), 'cumulative':0} for i in range(max_num_hands)]

    def callback(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result

    # 入力画像から手を検出
    def set_image(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image)
        timestamp = int(time.time()*1000)
        self.recognizer.recognize_async(mp_image, timestamp)

    # 結果を返す
    def get_results(self):
        return self.results

    def get_handedness(self):
        return len(self.results.handedness)

    # landmarkを返す
    def get_landmarks(self):
        if self.results.handedness:
            self.multi_landmarks = np.array([[[lms[i].x, lms[i].y] for i in range(20)] for lms in self.results.hand_landmarks])
        else:
            self.multi_landmarks = np.empty(0)
        return self.multi_landmarks

    # gestureを返す
    def get_gestures(self):
        if self.results.handedness:
            self.gesture = self.results.gestures[0][0].category_name
        else:
            self.gesture = 'empty'
        return self.gesture

    def get_image(self, bone=True, point=True, box=True, label=True, gesture=True):
        self.draw_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        if self.results.handedness:
            self.img_h, self.img_w = self.draw_image.shape[0:2]
            if bone:
                self.draw_landmark_bone()
            if point:
                self.draw_landmark_point()
            if box:
                self.draw_landmark_box()
            if label:
                self.draw_landmark_label()
            if gesture:
                self.draw_landmark_gesture()
        return self.draw_image

    def draw_landmark_bone(self):
        for lms in self.results.hand_landmarks:
            for bone in self.bone_link:
                for i in range(len(bone)-1):
                    pos1 = (int(lms[bone[i  ]].x*self.img_w), int(lms[bone[i  ]].y*self.img_h))
                    pos2 = (int(lms[bone[i+1]].x*self.img_w), int(lms[bone[i+1]].y*self.img_h))
                    cv2.line(self.draw_image, pos1, pos2, (0, 0, 255), thickness=2)

    def draw_landmark_point(self):
        for lms in self.results.hand_landmarks:
            for lm in lms:
                pos = (int(lm.x*self.img_w), int(lm.y*self.img_h))
                cv2.circle(self.draw_image, pos, 5, (255,0,0), thickness=-1)

    def draw_landmark_box(self):
        for lms in self.results.hand_landmarks:
            x_list = [lm.x for lm in lms]
            y_list = [lm.y for lm in lms]
            pos1  = (int(min(x_list)*self.img_w), int(min(y_list)*self.img_h))
            pos2  = (int(max(x_list)*self.img_w), int(max(y_list)*self.img_h))
            cv2.rectangle(self.draw_image, pos1, pos2, (255, 0, 0), thickness=2, lineType=cv2.LINE_8, shift=0)

    def draw_landmark_label(self):
        pass

    def draw_landmark_gesture(self):
        for i, (ges, lms) in enumerate(zip(self.results.gestures, self.results.hand_landmarks)):
            if ges[0].category_name == 'Closed_Fist':
                t = float(time.time()) - self.ges_time[i]['recognize']
                self.ges_time[i]['recognize'] = float(time.time())
                # 最終認識から0.5s以上経過
                if t > 0.5:
                    self.ges_time[i]['cumulative'] = 0
                else:
                    self.ges_time[i]['cumulative'] = min(1, self.ges_time[i]['cumulative'] + t)
                    x_list = [lm.x for lm in lms]
                    y_list = [lm.y for lm in lms]
                    norm = np.linalg.norm([(max(x_list)-min(x_list))*self.img_w, (max(y_list)-min(y_list))*self.img_h])/2
                    pos = (int((max(x_list)+min(x_list))/2*self.img_w), int((max(y_list)+min(y_list))/2*self.img_h))
                    size = norm*(3-2*self.ges_time[i]['cumulative'])
                    color = [int(c*255) for c in colorsys.hsv_to_rgb((2-self.ges_time[i]['cumulative'])/3, 1.0, 1.0)]
                    cv2.circle(self.draw_image, pos, int(size), color, thickness=2)

def main():
    hands = MPHand(max_num_hands=2)

    cap = cv2.VideoCapture(0)   # カメラのID指定

    if cap.isOpened():
        while True:
            # カメラから画像取得
            success, img = cap.read()
            if not success:
                break

            size = (640, 480)
            img = cv2.resize(img, size)     # リサイズ
            img = cv2.flip(img, 1)          # 画像を左右反転

            hands.set_image(img)
            if hands.get_results() is None:
                continue
            img = hands.get_image(bone=True, point=False, box=True, label=False, gesture=True)

            handedness = hands.get_handedness()

            size = (1280, 960)
            img = cv2.resize(img, size)     # リサイズ
            cv2.imshow('img', img)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

if __name__ == '__main__':
    main()
