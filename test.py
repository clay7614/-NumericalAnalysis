import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# データの設定
n_frames = 200  # フレーム数
grid_size = (11, 11)  # ヒートマップのサイズ

# 各フレームのデータを生成
data = [np.random.rand(*grid_size) for _ in range(n_frames)]

# 図の初期設定
fig, ax = plt.subplots()
cax = ax.imshow(data[0], cmap='viridis', interpolation='nearest')
fig.colorbar(cax)  # カラーバーを追加

# フレーム番号表示用のテキスト
frame_text = ax.text(0.02, 0.95, '', color='white', fontsize=12, 
                     transform=ax.transAxes, bbox=dict(facecolor='black', alpha=0.5))

# フレーム更新関数
def update(frame):
    cax.set_array(data[frame])  # ヒートマップデータの更新
    frame_text.set_text(f'Frame: {frame + 1}/{n_frames}')  # フレーム番号を更新
    return cax, frame_text

# アニメーション作成
ani = FuncAnimation(fig, update, frames=n_frames, interval=1, blit=True)

# アニメーション表示
plt.show()