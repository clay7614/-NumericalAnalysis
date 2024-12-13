import numpy as np
import sys
from tqdm import tqdm

#ユーザーが与える変数
x_spase = 5 #x軸のメッシュ数
y_spase = 5 #y軸のメッシュ数
z_spase = 5 #z軸のメッシュ数
time = 1  #時間区分数
d_time = 0.001  #時間変化量
loop = 10  #計算の反復回数

#自動的に算出する変数
dx_division = 1.0 / x_spase  #x軸のメッシュ間変化量
dy_division = 1.0 / y_spase  #y軸のメッシュ間変化量
dz_division = 1.0 / z_spase  #y軸のメッシュ間変化量
x_grids = x_spase + 1  #x軸の格子数
y_grids = x_spase + 1  #y軸の格子数
z_grids = z_spase + 1  #y軸の格子数
num_time = int(time / d_time)  #時間区分数

#解析に必要な配列を作成
thx_change = np.zeros((num_time, x_spase, y_spase, z_spase), dtype=np.float32)
thy_change = np.zeros((num_time, x_spase, y_spase, z_spase), dtype=np.float32)
thz_change = np.zeros((num_time, x_spase, y_spase, z_spase), dtype=np.float32)
tex_change = np.zeros((num_time, x_grids, y_grids, z_grids), dtype=np.float32)
tey_change = np.zeros((num_time, x_grids, y_grids, z_grids), dtype=np.float32)
tez_change = np.zeros((num_time, x_grids, y_grids, z_grids), dtype=np.float32)

#t=0の時の各メッシュの値を計算
"""
for i in range(x_grids):
    for j in range(y_grids):
        t_change[0][i][j] = 0
        #100 - 100 * np.sin(np.pi * x_division[i] * dx_division) * np.sin(np.pi * y_division[j] * dy_division)
        """

#境界条件の設定, boun = 境界の値
boun = 0
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

#np.save('np_save', t_change)