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

    counter = [0, 0]
    state = 'start'
    traj = np.empty((0,2))
    line = np.empty((0,2), dtype=int)
    angle = random.uniform(0, np.pi*2)
    speed = 10.0

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

            if traj.shape[0] == 0:
                traj = np.array([int(size[0]/2), int(size[1]/2)])
                for _ in range(15):
                    traj += np.array([int(np.cos(angle)*speed), int(np.sin(angle)*speed)])
                    np.clip(traj, 100, (size[0]-100, size[1]-100), out=traj)
                    line = np.append(line, [traj], axis=0)

                    if traj[0] <= 100:
                        angle = random.uniform(0, np.pi)
                    elif traj[0] >= size[0]-100:
                        angle = random.uniform(np.pi, np.pi*2)
                    elif traj[1] <= 100:
                        angle = random.uniform(np.pi/2, np.pi*3/2)
                    elif traj[1] >= size[1]-100:
                        angle = random.uniform(0, np.pi)-np.pi/2

            poses.set_image(img)
            if poses.get_results() is None:
                continue

            landmarks = poses.get_landmarks()

            if landmarks.shape[0] == 0:
                lm19 = (-100, -100)
                lm20 = (-100, -100)
            else:
                lm19 = (int(landmarks[0, 19, 0]*size[0]), int(landmarks[0, 19, 1]*size[1]))
                lm20 = (int(landmarks[0, 20, 0]*size[0]), int(landmarks[0, 20, 1]*size[1]))

                cv2.circle(img, lm19, 150, (255, 255, 255), thickness=3)
                cv2.circle(img, lm20, 150, (255, 255, 255), thickness=3)

            if state == 'start':
                cir = line[0]
                cv2.putText(img, 'Start with hand in the center', (int(size[0]*0.2), int(size[1]*0.7)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 200, 0), thickness=4)
                cv2.circle(img, cir, 100, (255, 200, 0), thickness=10)

                norm19 = np.linalg.norm(lm19 - cir)
                norm20 = np.linalg.norm(lm20 - cir)
                if min(norm19, norm20) < 150:
                    state = 'game'
                    time_start = time.time()

            elif state == 'game':
                traj += np.array([int(np.cos(angle)*speed), int(np.sin(angle)*speed)])
                np.clip(traj, 100, (size[0]-100, size[1]-100), out=traj)

                if traj[0] <= 100:
                    angle = random.uniform(0, np.pi)
                elif traj[0] >= size[0]-100:
                    angle = random.uniform(np.pi, np.pi*2)
                elif traj[1] <= 100:
                    angle = random.uniform(np.pi/2, np.pi*3/2)
                elif traj[1] >= size[1]-100:
                    angle = random.uniform(0, np.pi)-np.pi/2
                cir = line[0]
                cv2.circle(img, cir, 100, (255, 200, 0), thickness=10)

                line = np.delete(line, 0, 0)
                line = np.append(line, [traj], axis=0,)
                cv2.polylines(img, [line], False, (200, 100, 255), thickness=3, lineType=cv2.LINE_8, shift=0)

                norm19 = np.linalg.norm(lm19 - cir)
                norm20 = np.linalg.norm(lm20 - cir)
                if min(norm19, norm20) < 150:
                    counter[0] += 1
                else:
                    counter[1] += 1

                cv2.putText(img, f'{counter[0]/(counter[0]+counter[1])*100: .2f}%', (int(size[0]*0.4), int(size[1]*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 0, 255), thickness=4)

                dur = 30 - float(time.time()-time_start)
                if dur < 0:
                    state = 'result'
                elif dur > 10:
                    cv2.putText(img, f'{dur: .0f}', (int(size[0]*0.8), int(size[1]*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 2, (200, 200, 200), thickness=5)
                else:
                    cv2.putText(img, f'{dur: .1f}', (int(size[0]*0.8), int(size[1]*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 2, (200, 200, 200), thickness=5)

            elif state == 'result':
                cv2.putText(img, 'Result', (int(size[0]*0.4), int(size[1]*0.55)), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 0, 255), thickness=8)
                cv2.putText(img, f'{counter[0]/(counter[0]+counter[1])*100: .2f}%', (int(size[0]*0.25), int(size[1]*0.7)), cv2.FONT_HERSHEY_SIMPLEX, 5, (100, 0, 255), thickness=8)

            cv2.imshow('img', img)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

if __name__ == '__main__':
    main()
