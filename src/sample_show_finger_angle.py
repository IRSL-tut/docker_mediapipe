import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# landmark名
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

# 曲がり角
corner_side_ids = [
    [(1, 2, 3), (2, 3, 4)],         # 親指
    [(0, 5, 6), (5, 6, 7), (6, 7, 8)],         # 人差し指
    [(0, 9, 10), (9, 10, 11), (10, 11, 12)],    # 中指
    [(0, 13, 14), (13, 14, 15), (14,15, 16)],   # 薬指
    [(0, 17, 18), (17, 18, 19), (18, 19, 20)]    # 小指
]

def main():
    cap = cv2.VideoCapture(0)   # カメラのID指定
    frame = 0

    plt.ion()
    xs = [i-100 for i in range(100)]
    y1 = [0 for i in range(100)]
    y2 = [0 for i in range(100)]
    y3 = [0 for i in range(100)]
    y4 = [0 for i in range(100)]
    y5 = [0 for i in range(100)]
    fig, ax = plt.subplots()
    plt.grid()

    if cap.isOpened():
        while True:
            # カメラから画像取得
            success, img = cap.read()
            if not success:
                break

            frame += 1/cap.get(cv2.CAP_PROP_FPS)

            size = (1280, 960)
            img = cv2.resize(img, size)     # リサイズ
            img = cv2.flip(img, 1)          # 画像を左右反転
            img_h, img_w = img.shape[0:2]     # サイズ取得

            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            annotated_image = img.copy()

            results = hands.process(image)
            if results.multi_handedness:
                # 検出した手の数分繰り返し
                for h_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    x_list = []
                    y_list = []
                    z_list = []
                    for lm in hand_landmarks.landmark:
                        x_list.append(lm.x)
                        y_list.append(lm.y)
                        z_list.append(lm.z)
                    x_min = min(x_list)
                    x_max = max(x_list)
                    y_min = min(y_list)
                    y_max = max(y_list)
                    z_min = min(z_list)
                    z_max = max(z_list)

                    # 各指の曲がり角度を計算
                    angle_finger = []
                    is_open_finger = []
                    for corner_id, corners in enumerate(corner_side_ids):
                        degree = 0
                        for corner in corners:
                            # 点A,B,Cの座標（3次元座標上の場合）
                            a = np.array([x_list[corner[0]], y_list[corner[0]], z_list[corner[0]]])
                            b = np.array([x_list[corner[1]], y_list[corner[1]], z_list[corner[1]]])
                            c = np.array([x_list[corner[2]], y_list[corner[2]], z_list[corner[2]]])
                            # ベクトルを定義
                            vec_a = a - b
                            vec_b = b - c
                            # cosの計算
                            length_vec_a = np.linalg.norm(vec_a)
                            length_vec_c = np.linalg.norm(vec_b)
                            inner_product = np.inner(vec_a, vec_b)
                            cos = inner_product / (length_vec_a * length_vec_c)
                            # 角度（ラジアン）の計算
                            rad = np.arccos(cos)
                            # 弧度法から度数法（rad ➔ 度）への変換
                            degree += np.rad2deg(rad)
                        angle_finger.append(degree)
                        if corner_id == 0 and degree < 40:
                            is_open_finger.append(True)
                        elif corner_id != 0 and degree < 100:
                            is_open_finger.append(True)
                        else:
                            is_open_finger.append(False)

                    # グラフを表示
                    show_graph(angle_finger, ax, xs, y1, y2, y3, y4, y5)

                    # landmarkの繋がりをlineで表示
                    for line_id, landmarks in enumerate(landmark_line_ids):
                        for landmark in landmarks:
                            # 1点目座標取得
                            lm = hand_landmarks.landmark[landmark[0]]
                            lm_pos1 = (int(lm.x * img_w), int(lm.y * img_h))
                            # 2点目座標取得
                            lm = hand_landmarks.landmark[landmark[1]]
                            lm_pos2 = (int(lm.x * img_w), int(lm.y * img_h))
                            # line描画
                            cv2.line(annotated_image, lm_pos1, lm_pos2, landmark_line_colors[line_id], thickness=3)

                    # landmarkをcircleで表示
                    for point_id, landmarks in enumerate(landmark_point_ids):
                        for landmark in landmarks:
                            lm = hand_landmarks.landmark[landmark]
                            lm_pos = (int(lm.x * img_w), int(lm.y * img_h))
                            lm_z = int((z_max - lm.z) / (z_max - z_min) * 10 + 3)
                            cv2.circle(annotated_image, lm_pos, lm_z+1, (255, 255, 255), -1)
                            cv2.circle(annotated_image, lm_pos, lm_z, landmark_point_colors[point_id], -1)

                    # labelとscoreを表示
                    for c_id, hand_class in enumerate(results.multi_handedness[h_id].classification):
                        label = hand_class.label + ' {:.1f}%'.format(hand_class.score*100)
                    x_min = int(img_w*(x_min-0.02) if x_min>0 else 0)
                    y_min = int(img_h*(y_min-0.02) if y_min>0 else 0)
                    x_max = int(img_w*(x_max+0.02) if x_max<1 else img_w)
                    y_max = int(img_h*(y_max+0.02) if y_max<1 else img_h)
                    cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), thickness=2, lineType=cv2.LINE_8, shift=0)
                    cv2.fillConvexPoly(annotated_image, np.array(((x_min, y_min), (x_min+120, y_min), (x_min+100, y_min+20), (x_min, y_min+20))), (0, 255, 0))
                    cv2.putText(annotated_image, label, (x_min+5, y_min+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=1)
                    hand_id = "ID: " + str(h_id)
                    cv2.fillConvexPoly(annotated_image, np.array(((x_max, y_max), (x_max-60, y_max), (x_max-40, y_max-20), (x_max, y_max-20))), (0, 255, 0))
                    cv2.putText(annotated_image, hand_id, (x_max-40, y_max-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), thickness=1)
                    for f_id, is_open in enumerate(is_open_finger):
                        if is_open:
                            cv2.circle(annotated_image, (int((x_min+x_max)/2-100+f_id*50), y_min-30), 20, (0, 0, 255), -1)
                        else:
                            cv2.circle(annotated_image, (int((x_min+x_max)/2-100+f_id*50), y_min-30), 20, (0, 0, 255), 5)

            cv2.imshow('img', annotated_image)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('s') or key == ord('S') or key == 0x1b:
                image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                plt.imsave('./image.jpg', image)
                print("saved!")
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

# グラフを表示
def show_graph(angle_finger, ax, xs, y1, y2, y3, y4, y5):
    y1.append(angle_finger[0])
    y2.append(angle_finger[1])
    y3.append(angle_finger[2])
    y4.append(angle_finger[3])
    y5.append(angle_finger[4])
    if len(y1) > 100:
        y1.pop(0)
        y2.pop(0)
        y3.pop(0)
        y4.pop(0)
        y5.pop(0)
    # グラフ描画
    line1, = ax.plot(xs, y1, color='C0', linestyle='-', label='1')
    line2, = ax.plot(xs, y2, color='C1', linestyle='-', label='2')
    line3, = ax.plot(xs, y3, color='C2', linestyle='-', label='3')
    line4, = ax.plot(xs, y4, color='C3', linestyle='-', label='4')
    line5, = ax.plot(xs, y5, color='C4', linestyle='-', label='5')

    ax.set_xlim(-100, 0)
    ax.set_ylim(0, 360)
    ax.set_xlabel('Time [$frame$]')
    ax.set_ylabel('angle [$deg$]')
    plt.pause(0.001)
    line1.remove()
    line2.remove()
    line3.remove()
    line4.remove()
    line5.remove()

if __name__ == '__main__':
    main()