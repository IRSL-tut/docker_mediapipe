# mediapipe pose
# https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python

import colorsys
import os
import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class MPPose():
    def __init__(self, model='full', max_num_poses=1, min_detection_confidence=0.5, min_pose_presence_confidence=0.5, min_tracking_confidence=0.5, running_mode='LIVE_STREAM'):
        """MediaPipeを用いたPoseの検出クラス

        Args:
            model (str,optional): 使用するタスク({'lite', 'full', 'heavy'}). Default to 'full'.
            max_num_poses (int, optional): 検出するポーズの最大数(Any integer > 0). Defaults to 1.
            min_detection_confidence (float, optional): ポーズ検出モデルで成功したとみなされるポーズの検出の最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
            min_pose_presence_confidence (float, optional): ポーズランドマーク検出モデルにおけるポーズ存在スコアの最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
            min_tracking_confidence (float, optional): ポーズトラッキングが成功したとみなされるための最小信頼スコア(0.0 ~ 1.0). Defaults to 0.5.
            running_mode (str, optional): タスクの実行モード({'IMAGE', 'VIDEO', 'LIVE_STREAM'}). Defaults to 'LIVE_STREAM'.
        """

        model_path = os.path.dirname(os.path.abspath(__file__)) + '/task/pose_landmarker_'+model+'.task'   #'./task/pose_landmarker_{model}.task'
        base_options = python.BaseOptions(model_asset_path=model_path)
        VisionRunningMode = vision.RunningMode
        if running_mode == 'IMAGE':
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                running_mode=VisionRunningMode.IMAGE,
                num_poses=max_num_poses,
                min_pose_detection_confidence=min_detection_confidence,
            )
        elif running_mode == 'VIDEO':
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                running_mode=VisionRunningMode.VIDEO,
                num_poses=max_num_poses,
                min_pose_detection_confidence=min_detection_confidence,
                min_pose_presence_confidence=min_pose_presence_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
        elif running_mode == 'LIVE_STREAM':
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                running_mode=VisionRunningMode.LIVE_STREAM,
                result_callback=self.callback,
                num_poses=max_num_poses,
                min_pose_detection_confidence=min_detection_confidence,
                min_pose_presence_confidence=min_pose_presence_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
        else:
            print(f'unknown running mode "{running_mode}"')
            return
        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.running_mode = running_mode
        self.results = None
        self.visual = VisualizePoseInfo()

    def callback(self, result: vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result

    # 入力画像からポーズを検出
    def set_image(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image)
        if self.running_mode == 'IMAGE':
            self.results = self.landmarker.detect(mp_image)
        elif self.running_mode == 'VIDEO':
            timestamp = int(time.time()*1000)
            self.results = self.landmarker.detect_for_video(mp_image, timestamp)
        elif self.running_mode == 'LIVE_STREAM':
            timestamp = int(time.time()*1000)
            self.landmarker.detect_async(mp_image, timestamp)

    # 結果を返す
    def get_results(self):
        return self.results

    # landmarkを返す
    def get_landmarks(self):
        if self.results.pose_landmarks:
            multi_landmarks = np.array([
                [
                    [lm.x, lm.y] for lm in lms
                ] for lms in self.results.pose_landmarks
            ])
        else:
            multi_landmarks = np.empty(0)
        return multi_landmarks

    def add_results_to_image(self, image, **kwargs):
        """
        kwargs: bone=False, point=False
        """
        return self.visual.get_image(image,
                                     self.get_landmarks(),
                                     **kwargs)

class VisualizePoseInfo():
    def __init__(self):
        self.draw_image = None
        self.height = None
        self.width = None

        self.bone_link = [
            [7,3,2,1,0,4,5,6,8], ## eyes
            [9,10],              ## mouse
            [11,12,24,23,11],    ## body
            [11,13,15,17,19,15,21], ## left-arm
            [12,14,16,18,20,16,22], ## right-arm
            [23,25,27,29,31,27], ## left-leg
            [24,26,28,30,32,28], ## right-leg
        ]
#  0 - nose
#  1 - left eye (inner)
#  2 - left eye
#  3 - left eye (outer)
#  4 - right eye (inner)
#  5 - right eye
#  6 - right eye (outer)
#  7 - left ear
#  8 - right ear
#  9 - mouth (left)
# 10 - mouth (right)
# 11 - left shoulder
# 12 - right shoulder
# 13 - left elbow
# 14 - right elbow
# 15 - left wrist
# 16 - right wrist
# 17 - left pinky
# 18 - right pinky
# 19 - left index
# 20 - right index
# 21 - left thumb
# 22 - right thumb
# 23 - left hip
# 24 - right hip
# 25 - left knee
# 26 - right knee
# 27 - left ankle
# 28 - right ankle
# 29 - left heel
# 30 - right heel
# 31 - left foot index
# 32 - right foot index

        self.color = {
            'red'  : (0, 0, 255),
            'green': (0, 255, 0),
            'blue' : (255, 0, 0),
        }

    # 描画後の画像を返す
    def get_image(self, image, landmarks,
                  bone=False, point=False):
        self.draw_image = image
        self.height, self.width = self.draw_image.shape[0:2]
        if bone:
            self.draw_landmark_bone(landmarks)
        if point:
            self.draw_landmark_point(landmarks)
        return self.draw_image

    def draw_landmark_bone(self, landmarks):
        for lms in landmarks:
            for bone in self.bone_link:
                for i in range(len(bone)-1):
                    pos1 = (int(lms[bone[i  ]][0]*self.width), int(lms[bone[i  ]][1]*self.height))
                    pos2 = (int(lms[bone[i+1]][0]*self.width), int(lms[bone[i+1]][1]*self.height))
                    cv2.line(self.draw_image, pos1, pos2, self.color['red'], thickness=3)

    def draw_landmark_point(self, landmarks):
        for lms in landmarks:
            for lm in lms:
                pos = (int(lm[0]*self.width), int(lm[1]*self.height))
                size = 5
                cv2.circle(self.draw_image, pos, size, self.color['blue'], thickness=-1)
