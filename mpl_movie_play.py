import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

result_array = np.load("movie_save.npy")
result_array_len = len(result_array)

#図の初期設定
fig, ax = plt.subplots()
cax = ax.imshow(result_array[0], cmap='gray', interpolation='nearest', vmin=0, vmax=255)
ax.axis('off')

#フレーム番号表示用のテキスト
frame_text = ax.text(0.02, 0.95, '', color='white', fontsize=12,
                    transform=ax.transAxes, bbox=dict(facecolor='black', alpha=0.5))

speed = 1 #再生速度

#フレーム更新関数
def update(frame):
    cax.set_array(result_array[int(frame * speed)])
    frame_text.set_text(f'Frame: {frame * speed}/{result_array_len}')
    return cax, frame_text

#アニメーション
ani = FuncAnimation(fig, update, frames=int(result_array_len / speed), interval=15, blit=True)
plt.show()