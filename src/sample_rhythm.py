import random
import time

import cv2
import numpy as np

from mppack import mp_pose

"""
リズムゲームサンプル
"""

def main():
    poses = mp_pose.MPPose(max_num_poses=1)

    diff = 2.0
    time_frame = time.time()
    timer = 0
    counter = 0
    text = ''
    arr = np.empty((0,3))

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

            poses.set_image(img)
            if poses.get_results() is None:
                continue

            landmarks = poses.get_landmarks()

            timer -= time.time() - time_frame
            if timer <= 0:
                arr = np.append(arr,
                                np.array([[
                                    random.randint(0, size[0]),
                                    random.randint(0, size[1]),
                                    float(time.time()),
                                ]]),
                                axis=0,
                )
                timer = diff

            if landmarks.shape[0] == 0:
                m19 = (-100, -100)
                m20 = (-100, -100)
            else:
                lm19 = (int(landmarks[0, 19, 0]*size[0]), int(landmarks[0, 19, 1]*size[1]))
                lm20 = (int(landmarks[0, 20, 0]*size[0]), int(landmarks[0, 20, 1]*size[1]))

                cv2.circle(img, lm19, 100, (255, 255, 255), thickness=3)
                cv2.circle(img, lm20, 100, (255, 255, 255), thickness=3)

            for i, a in enumerate(arr):
                dur = float(time.time()) - a[2]
                if  dur > diff:
                    norm19 = np.linalg.norm(lm19 - a[0:2])
                    norm20 = np.linalg.norm(lm20 - a[0:2])
                    if min(norm19, norm20) < 100:
                        text = 'perfect'
                        counter += 1
                    else:
                        text = ' miss'
                        counter = 0
                    arr = np.delete(arr, i, 0)
                else:
                    pos = (int(a[0]), int(a[1]))
                    s = int((diff - dur)* (200/ diff))
                    cv2.circle(img, pos, s, (100, 40, 255), thickness=3)

            cv2.putText(img, text, (int(size[0]*0.4), int(size[1]*0.9)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 200, 0), thickness=8)
            if counter > 0:
                cv2.putText(img, str(counter)+'combo', (int(size[0]*0.8), int(size[1]*0.8)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 255), thickness=3)
            cv2.imshow('img', img)

            time_frame = time.time()

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

if __name__ == '__main__':
    main()
