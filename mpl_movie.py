import cv2
import numpy as np
from tqdm import tqdm

#動画ファイルを読み込む
video_path = "SummerPockets.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("動画を開けませんでした")
else:
    #フレーム数と解像度を取得
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"フレーム数={frame_count}, 幅={width}, 高さ={height}")

    #全フレームのBWを格納する配列
    result_array = np.zeros((frame_count, height, width), dtype=np.uint8)

    #各フレームを処理
    current_frame = 0
    with tqdm(total = frame_count, desc="動画処理", ncols=80, leave=False) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  #フレームが取得できなくなったら終了

            #グレースケールに変換
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #結果を格納
            result_array[current_frame, :, :] = gray_frame
            current_frame += 1
            pbar.update(1)

cap.release()

np.save('movie_save', result_array)