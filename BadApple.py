import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

#動画ファイルを読み込む
video_path = "BadApple.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("動画を開けませんでした")
else:
    #フレーム数と解像度を取得
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"フレーム数={frame_count}, 幅={width}, 高さ={height}")

    #全フレームのRGB強度を格納する配列
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

            #二値化処理
            _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

            #結果を格納
            result_array[current_frame, :, :] = binary_frame
            current_frame += 1
            pbar.update(1)

cap.release()

#図の初期設定
fig, ax = plt.subplots()
cax = ax.imshow(result_array[0], cmap='CMRmap', interpolation='nearest', vmin=0, vmax=255)
ax.axis('off')

#フレーム番号表示用のテキスト
frame_text = ax.text(0.02, 0.95, '', color='white', fontsize=12,
                    transform=ax.transAxes, bbox=dict(facecolor='black', alpha=0.5))

speed = 1 #再生速度

#フレーム更新関数
def update(frame):
    cax.set_array(result_array[int(frame * speed)])
    frame_text.set_text(f'Frame: {frame * speed}/{frame_count}')
    return cax, frame_text

#アニメーション
ani = FuncAnimation(fig, update, frames=int(frame_count / speed), interval=15, blit=True)
plt.show()