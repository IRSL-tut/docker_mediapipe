#!/usr/bin/env python3
# coding: utf-8
import cv2
import numpy as np
from mppack import mp_hand
from mppack import mp_pose
from mppack import camera_capture

cap = camera_capture.CvCapture(0)

img = cap.capture()
img = cap.capture()
cap.show(img)

### 手の認識モデル生成
hand_recog = mp_hand.MPHand(max_num_hands=1, running_mode='IMAGE')
hand_recog.set_image(img)

# res = hand_recog.get_results()
rimg = hand_recog.add_results_to_image(img, bone=True, point=True, box=True, circle=True, box_palm=True)
cap.show(rimg)


### 全身の認識モデル生成
pose_recog = mp_pose.MPPose(max_num_poses=1, running_mode='IMAGE')
pose_recog.set_image(img)

# res = pose_recog.get_results()
rimg = pose_recog.add_results_to_image(img, bone=True, point=True)
cap.show(rimg)
