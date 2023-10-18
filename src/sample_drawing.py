import cv2
import numpy as np
from mppack import mp_hand

"""
お絵描きサンプル
"""

def main():
    hands = mp_hand.MPHand(max_num_hands=1) # 手の認識モデル生成

    canvas = None # キャンバス用変数

    cap = cv2.VideoCapture(0)   # カメラのID指定

    if cap.isOpened():
        while True:
            # カメラから画像取得
            success, img = cap.read()
            if not success:
                break

            size = (1280, 960)              # 画像サイズの指定
            img = cv2.resize(img, size)     # リサイズ
            img = cv2.flip(img, 1)          # 画像を左右反転

            # 画像サイズに合わせてキャンバス生成
            if canvas is None:
                canvas = np.zeros(img.shape[:], dtype=img.dtype)

            # 手の認識モデルに画像をセット
            hands.set_image(img)
            if hands.get_results() is None:
                continue

            # モデルからデータを取得
            handedness = hands.get_handedness()         # 手の左右(0: 右手, 1:左手)
            landmarks = hands.get_landmarks()           # 手のランドマーク(array[個数, 31点, 3D座標])
            gestures = hands.get_gestures()             # 手のジェスチャー({"None", "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"})
            duration = hands.get_gestures_duration()    # ジェスチャーを認識し続けた時間(float)

            # 認識した手を1つづつ処理
            for hand, lms, ges, dur in zip(handedness, landmarks, gestures, duration):
                # ジェスチャーが Pointing_Up のとき
                if ges == "Pointing_Up" and dur > 0.5:
                    pos = (int(lms[8][0]*size[0]), int(lms[8][1]*size[1]))
                    cv2.circle(canvas, pos, 15, (100, 40, 255), thickness=-1)
                # ジェスチャーが Open_Palm のとき
                if ges == "Open_Palm" and dur > 0.5:
                    pos = (int(lms[9][0]*size[0]), int(lms[9][1]*size[1]))
                    cv2.circle(canvas, pos, 150, (0, 0, 0), thickness=-1)
                    cv2.circle(img, pos, 150, (255, 255, 255), thickness=3)

            # キャンバスを合成
            img = np.where(canvas == 0, img, canvas)

            # 画像出力
            cv2.imshow('img', img)

            # キー入力認識
            key = cv2.waitKey(10) & 0xFF
            # Qキーで終了
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

if __name__ == '__main__':
    main()
