import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import japanize_matplotlib
import sys
from tqdm import tqdm

# ユーザーが与える変数
x_spase = 50 # x軸のメッシュ数
y_spase = 50 # y軸のメッシュ数
time = 1  # 時間区分数
d_time = 0.00001  # 時間変化量
loop = 10  # 計算の反復回数
ppv = 1 # 物性値

# 自動的に算出する変数
dx_division = 1.0 / x_spase  # x軸のメッシュ間変化量
dy_division = 1.0 / y_spase  # y軸のメッシュ間変化量
x_grids = x_spase + 1  # x軸の格子数
y_grids = x_spase + 1  # y軸の格子数
num_time = int(time / d_time)  # 時間区分数
ppv_list = np.zeros((x_grids, y_grids)) #物性値リスト

x_solution = d_time / np.power(dx_division, 2)
y_solution = d_time / np.power(dy_division, 2)

if x_solution > 0.5 or y_solution > 0.5:
    sys.exit("'Δt/Δ^2x'の値が" + str(x_solution) +" , "+ str(y_solution) + "になり解析結果が発散します。")

# 解析に必要な配列を作成
t_change = np.zeros((num_time, y_grids, x_grids), dtype=np.float32)
x_division = np.array(range(x_grids))
y_division = np.array(range(y_grids))

# t=0の時の各メッシュの値を計算
"""
for i in range(x_grids):
    for j in range(y_grids):
        t_change[0][i][j] = 0
        #100 - 100 * np.sin(np.pi * x_division[i] * dx_division) * np.sin(np.pi * y_division[j] * dy_division)
        """

for i in range(x_grids):
    for j in range(y_grids):
        if y_grids*0.4 <= j | j <= y_grids*0.6:
            ppv_list[i][j] = 1
        else:
            ppv_list[i][j] = 0.05


#境界条件の設定, boun = 境界の値
boun = 40
for i in range(num_time):
    for j in x_division:
        t_change[i][0][j] = boun
        t_change[i][x_spase][j] = boun
for i in range(num_time):
    for j in y_division:
        t_change[i][j][0] = boun
        t_change[i][j][y_spase] = boun

#シミュレーションプログラム
for _ in tqdm(range(loop), desc="proc1", ncols=80):
    for n in tqdm(range(len(t_change) - 1), desc="proc2", ncols=80, leave=False):
        t_change[n+1, 1:-1, 1:-1] = (
                t_change[n, 1:-1, 1:-1]
                + x_solution * ppv_list[1:-1, 1:-1] * (t_change[n, 2:, 1:-1] - 2 * t_change[n, 1:-1, 1:-1] + t_change[n, :-2, 1:-1])
                + y_solution * ppv_list[1:-1, 1:-1] * (t_change[n, 1:-1, 2:] - 2 * t_change[n, 1:-1, 1:-1] + t_change[n, 1:-1, :-2])
            )

        """
        for i in x_division[1:-1]:
            for j in y_division[1:-1]:
                t_change[n+1][i][j] = (t_change[n][i][j] + x_solution * (t_change[n][i+1][j] - 2 * t_change[n][i][j] + t_change[n][i-1][j])
                                       + y_solution * (t_change[n][i][j+1] - 2 * t_change[n][i][j] + t_change[n][i][j-1]))
        """

np.save('np_save', t_change)

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