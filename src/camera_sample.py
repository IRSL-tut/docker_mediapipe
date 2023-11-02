#!/usr/bin/env python3
# coding: utf-8
import cv2
import numpy as np
from mppack import mp_hand
from mppack import mp_pose
from mppack import camera_capture

cap = camera_capture.CvCapture(0)

img = cap.capture()
cap.show(img)

## 遅延キャプチャ
img = cap.capture(delay=1.0); cap.show(img)

### 手の認識モデル生成
hand_recog = mp_hand.MPHand(max_num_hands=1, running_mode='IMAGE')
hand_recog.set_image(img)
land = hand_recog.get_landmarks()

hand_recog.set_image(img_und)
land_und = hand_recog.get_landmarks()

# res = hand_recog.get_results()
cap.show(hand_recog.add_results_to_image(img_und, bone=True, point=True, box=True, circle=True, box_palm=True, copy=True))

### 認識結果の保存
hand_recog.write_results(img, 'hand000')

### 全身の認識モデル生成
pose_recog = mp_pose.MPPose(max_num_poses=1, running_mode='IMAGE')
pose_recog.set_image(img)

# res = pose_recog.get_results()
rimg = pose_recog.add_results_to_image(img, bone=True, point=True, copy=True)
cap.show(rimg)

### 認識結果の保存
pose_recog.write_results(img, 'pose000')

## 認識結果の確認
res = hand_recog.get_results()

hand_landmarks = res.hand_landmarks

len(hand_landmarks) ## num of hands

hand_landmarks0 = hand_landmarks[0]

len(hand_landmarks0) ## num of landmark

landmark = hand_landmarks0[0]

print(landmark.x, landmark.y, landmark.z)
