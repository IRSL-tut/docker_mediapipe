import cv2
from mppack import mp_hand

def main():
    hands = mp_hand.MPHand(max_num_hands=2)
    visualizer = mp_hand.VisualizeHandInfo()

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

            handedness = hands.get_handedness()
            landmarks = hands.get_landmarks()
            gestures = hands.get_gestures()
            duration = hands.get_gestures_duration()
            img = visualizer.get_image(img, handedness, landmarks, gestures, duration, bone=True, point=True, box=True, circle=True, box_palm=True)

            size = (1280, 960)
            img = cv2.resize(img, size)     # リサイズ
            cv2.imshow('img', img)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

if __name__ == '__main__':
    main()
