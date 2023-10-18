import cv2
import os
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = os.path.dirname(os.path.abspath(__file__)) + '/mppack/task/gesture_recognizer.task'
base_options = python.BaseOptions(model_asset_path=model_path)
VisionRunningMode = vision.RunningMode
options = vision.GestureRecognizerOptions(base_options=base_options,
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.3,
    min_tracking_confidence=0.5,)
recognizer = vision.GestureRecognizer.create_from_options(options)

# # landmark名
list_landmark = [
    'WRIST', 'THUMP_CMC',
    'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
    'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP', 'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP',
    'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP',
    'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
    'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
]

# landmarkの点表示用
landmark_point_ids = [
    [0, 1, 5, 9, 13, 17],
    [2, 3, 4],
    [6, 7, 8],
    [10, 11, 12],
    [14, 15, 16],
    [18, 19, 20]
]

# landmarkの点の色
landmark_point_colors = [
    (0, 0, 255),
    (213, 239, 255),
    (128, 0, 128),
    (0, 220, 255),
    (0, 255, 0),
    (255, 0, 0)
]

# landmarkの繋がり表示用
landmark_line_ids = [
    [(0, 1), (1, 5), (5, 9), (9, 13), (13, 17), (17, 0)],  # 掌
    [(1, 2), (2, 3), (3, 4)],         # 親指
    [(5, 6), (6, 7), (7, 8)],         # 人差し指
    [(9, 10), (10, 11), (11, 12)],    # 中指
    [(13, 14), (14, 15), (15, 16)],   # 薬指
    [(17, 18), (18, 19), (19, 20)]    # 小指
]

# landmarkの繋がりの色
landmark_line_colors = [
    (128, 128, 128),
    (213, 239, 255),
    (128, 0, 128),
    (0, 220, 255),
    (0, 255, 0),
    (255, 0, 0)
]

cap = cv2.VideoCapture(0)   # カメラのID指定
if cap.isOpened():
    while True:
        # カメラから画像取得
        success, img = cap.read()
        if not success:
            break

        size = (1280, 960)
        img = cv2.resize(img, size)     # リサイズ

        img = cv2.flip(img, 1)          # 画像を左右反転
        img_h, img_w = img.shape[0:2]     # サイズ取得
        # print(img_h, img_w)

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        results = recognizer.recognize(mp_image)
        # print(results)

        annotated_image = img.copy()
        if results.handedness:
            # print(results.handedness)
            # 検出した手の数分繰り返し
            for h_id, hand_landmarks in enumerate(results.hand_landmarks):
                # print(hand_landmarks)
                x_list = [hand_landmarks[i].x for i in range(20)]
                x_min = min(x_list)
                x_max = max(x_list)
                y_list = [hand_landmarks[i].y for i in range(20)]
                y_min = min(y_list)
                y_max = max(y_list)
                z_list = [hand_landmarks[i].z for i in range(20)]
                z_min = min(z_list)
                z_max = max(z_list)

                # contour = np.array([[int(lm.x * img_w), int(lm.y * img_h)] for lm in hand_landmarks.landmark])
                # rect = cv2.minAreaRect(contour)
                # box = cv2.boxPoints(rect)
                # box = np.intp(box)
                # cv2.drawContours(annotated_image,[box],0,(0,0,255), 2)

                # landmarkの繋がりをlineで表示
                for line_id, landmarks in enumerate(landmark_line_ids):
                    for landmark in landmarks:
                        # 1点目座標取得
                        lm = hand_landmarks[landmark[0]]
                        lm_pos1 = (int(lm.x * img_w), int(lm.y * img_h))
                        # 2点目座標取得
                        lm = hand_landmarks[landmark[1]]
                        lm_pos2 = (int(lm.x * img_w), int(lm.y * img_h))
                        # line描画
                        cv2.line(annotated_image, lm_pos1, lm_pos2, landmark_line_colors[line_id], thickness=3)

                # landmarkをcircleで表示
                for point_id, landmarks in enumerate(landmark_point_ids):
                    for landmark in landmarks:
                        lm = hand_landmarks[landmark]
                        lm_pos = (int(lm.x * img_w), int(lm.y * img_h))
                        lm_z = int((z_max - lm.z) / (z_max - z_min) * 10 + 3)
                        cv2.circle(annotated_image, lm_pos, lm_z+1, (255, 255, 255), -1)
                        cv2.circle(annotated_image, lm_pos, lm_z, landmark_point_colors[point_id], -1)

                # labelとscoreを表示
                for c_id, hand_class in enumerate(results.handedness[h_id]):
                    # print(hand_class)
                    label = hand_class.category_name + ' {:.1f}%'.format(hand_class.score*100)

                # gestureを表示
                for c_id, hand_gestures in enumerate(results.gestures[h_id]):
                    gesture = hand_gestures.category_name

                x_min = int(img_w*(x_min-0.02) if x_min>0 else 0)
                y_min = int(img_h*(y_min-0.02) if y_min>0 else 0)
                x_max = int(img_w*(x_max+0.02) if x_max<1 else img_w)
                y_max = int(img_h*(y_max+0.02) if y_max<1 else img_h)
                cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), thickness=2, lineType=cv2.LINE_8, shift=0)
                cv2.fillConvexPoly(annotated_image, np.array(((x_min, y_min), (x_min+120, y_min), (x_min+100, y_min+20), (x_min, y_min+20))), (0, 255, 0))
                cv2.fillConvexPoly(annotated_image, np.array(((x_max, y_max), (x_max-120, y_max), (x_max-100, y_max-20), (x_max, y_max-20))), (0, 255, 0))
                cv2.putText(annotated_image, label, (x_min+5, y_min+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=1)
                cv2.putText(annotated_image, gesture, (x_max-95, y_max), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=1)

        cv2.imshow('img', annotated_image)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('s') or key == ord('S') or key == 0x1b:
            image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            plt.imsave('./image.jpg', image)
            print("saved!")
        if key == ord('q') or key == ord('Q') or key == 0x1b:
            break