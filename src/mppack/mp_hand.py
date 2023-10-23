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
        """MediaPipeを用いた手の検出クラス

        Args:
            max_num_hands (int, optional): 検出する手の最大数(Any integer > 0). Defaults to 1.
            min_detection_confidence (float, optional): 手のひら検出モデルで成功したとみなされる手の検出の最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
            min_hand_presence_confidence (float, optional): 手のランドマーク検出モデルにおける手の存在スコアの最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
            min_tracking_confidence (float, optional): ハンドトラッキングが成功したとみなされるための最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
        """

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

        self.ges_list = ['None', 'Closed_Fist', 'Open_Palm', 'Pointing_Up', 'Thumb_Down', 'Thumb_Up', 'Victory', 'ILoveYou']
        t = float(time.time())
        self.ges_time = [{g:{'recognize':t, 'duration':0} for g in self.ges_list} for _ in range(2)]

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

    # 手の左右を返す
    def get_handedness(self):
        index = np.array([i[0].index for i in self.results.handedness])
        return index

    # landmarkを返す
    def get_landmarks(self):
        if self.results.handedness:
            multi_landmarks = np.array([
                [
                    [lm.x, lm.y] for lm in lms
                ] for lms in self.results.hand_landmarks
            ])
        else:
            multi_landmarks = np.empty(0)
        return multi_landmarks

    # gestureを返す
    def get_gestures(self):
        gestures = [ges[0].category_name for ges in self.results.gestures]
        return gestures

    # gesture継続時間を返す
    def get_gestures_duration(self):
        gestures_duration = []
        for hand, ges in zip(self.results.handedness, self.results.gestures):
            index = hand[0].index
            gesture = ges[0].category_name
            t0 = float(time.time())
            for g in self.ges_list:
                t = t0 - self.ges_time[index][g]['recognize']
                # 最終認識から0.5s以上経過
                if t > 0.5:
                    self.ges_time[index][g]['duration'] = 0
                    t = 0
                if g == gesture:
                    self.ges_time[index][g]['recognize'] = t0
                    self.ges_time[index][g]['duration'] += t
                    gestures_duration.append(self.ges_time[index][g]['duration'])
        return gestures_duration



class VisualizeHandInfo():
    def __init__(self):
        self.draw_image = None
        self.height = None
        self.width = None

        self.bone_link = [
            [0,1,2,3,4],
            [1,5,6,7,8],
            [9,10,11,12],
            [13,14,15,16],
            [0,17,18,19,20],
            [5,9,13,17],
        ]

        self.color = {
            'red'  : (0, 0, 255),
            'green': (0, 255, 0),
            'blue' : (255, 0, 0),
        }

    # 描画後の画像を返す
    def get_image(self, image, handedness, landmarks, gestures, duration,
                    bone=False, point=False, box=False, circle=False, box_palm=False):
        self.draw_image = image
        self.height, self.width = self.draw_image.shape[0:2]
        if bone:
            self.draw_landmark_bone(landmarks)
        if point:
            self.draw_landmark_point(landmarks)
        if box:
            self.draw_landmark_box(landmarks)
        if circle:
            self.draw_circle(landmarks, gestures, duration)
        if box_palm:
            self.draw_box_palm(landmarks)
        return self.draw_image

    def draw_landmark_bone(self, landmarks):
        for lms in landmarks:
            for bone in self.bone_link:
                for i in range(len(bone)-1):
                    pos1 = (int(lms[bone[i  ]][0]*self.width), int(lms[bone[i  ]][1]*self.height))
                    pos2 = (int(lms[bone[i+1]][0]*self.width), int(lms[bone[i+1]][1]*self.height))
                    cv2.line(self.draw_image, pos1, pos2, self.color['red'], thickness=2)

    def draw_landmark_point(self, landmarks):
        for lms in landmarks:
            for lm in lms:
                pos = (int(lm[0]*self.width), int(lm[1]*self.height))
                size = 2
                cv2.circle(self.draw_image, pos, size, self.color['blue'], thickness=-1)

    def draw_landmark_box(self, landmarks):
        for lms in landmarks:
            x_list = [lm[0] for lm in lms]
            y_list = [lm[1] for lm in lms]
            pos1  = (int(min(x_list)*self.width), int(min(y_list)*self.height))
            pos2  = (int(max(x_list)*self.width), int(max(y_list)*self.height))
            color = self.color['green']
            cv2.rectangle(self.draw_image, pos1, pos2, color, thickness=2, lineType=cv2.LINE_8, shift=0)

    def draw_circle(self, landmarks, gestures, duration):
        for lms, ges, dur in zip(landmarks, gestures, duration):
            if ges == 'Closed_Fist':
                x_list = [lm[0] for lm in lms]
                y_list = [lm[1] for lm in lms]
                x_max = max(x_list)
                x_min = min(x_list)
                y_max = max(y_list)
                y_min = min(y_list)
                t = min(dur, 1)
                norm = np.linalg.norm([(x_max-x_min)*self.width, (y_max-y_min)*self.height])/2
                pos = (int((x_max+x_min)/2*self.width), int((y_max+y_min)/2*self.height))
                size = int(norm*(3-2*t))
                color = [int(c*255) for c in colorsys.hsv_to_rgb((2-t)/3, 1.0, 1.0)]
                cv2.circle(self.draw_image, pos, size, color, thickness=2)

    def draw_box_palm(self, landmarks):
        for lms in landmarks:
            points = np.array([
                [int(lms[i][0]*self.width), int(lms[i][1]*self.height)] for i in (0, 1, 5, 9, 13, 17)
            ], dtype = np.int32)
            rect = cv2.minAreaRect(points)
            box = [np.int0(cv2.boxPoints(rect))]
            color = (255, 0, 0)
            cv2.polylines(self.draw_image, box, True, color, thickness=2, lineType=cv2.LINE_8, shift=0)