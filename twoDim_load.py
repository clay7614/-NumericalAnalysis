import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import japanize_matplotlib
from tqdm import tqdm

t_change = np.load('np_save.npy')

x_spase = 50 # x軸のメッシュ数
y_spase = 50 # y軸のメッシュ数
time = 1  # 時間区分数
d_time = 0.0001  # 時間変化量
loop = 10  # 計算の反復回数
ppv = 1 # 物性値

# 自動的に算出する変数
dx_division = 1.0 / x_spase  # x軸のメッシュ間変化量
dy_division = 1.0 / y_spase  # y軸のメッシュ間変化量
x_grids = x_spase + 1  # x軸の格子数
y_grids = x_spase + 1  # y軸の格子数
num_time = int(time / d_time)  # 時間区分数
ppv_list = np.zeros((x_grids, y_grids)) #物性値リスト

X, Y = np.mgrid[0:x_grids, 0:y_grids]
X, Y = np.round(X * dx_division, 3), np.round(Y * dy_division, 3)

# 図の初期設定
fig, ax = plt.subplots()
cax = ax.imshow(t_change[0], cmap='CMRmap', interpolation='nearest')
fig.colorbar(cax)  # カラーバーを追加

# フレーム番号表示用のテキスト
frame_text = ax.text(0.02, 0.95, '', color='white', fontsize=12,
                    transform=ax.transAxes, bbox=dict(facecolor='black', alpha=0.5))

speed = int(num_time / 200) #再生速度

# フレーム更新関数
def update(frame):
    cax.set_array(t_change[int(frame * speed)])
    frame_text.set_text(f'time: {round((frame * speed) * d_time, 4)}/{time}')  # フレーム番号を更新
    return cax, frame_text

# アニメーション作成
ani = FuncAnimation(fig, update, frames=int(num_time / speed), interval=0, blit=True)

# アニメーション表示
plt.show()