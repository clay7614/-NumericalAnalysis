import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.animation as animation
import sys
from tqdm import tqdm

#ユーザーが与える変数
spase = 10 #メッシュ数
time = 1 #時間区分数
d_time = 0.005 #時間変化量
loop = 100 #計算の反復回数

#自動的に算出する変数
d_division = 1.0 / spase #メッシュ間変化量
grids = spase + 1 #1格子数
x_time = int(time/d_time) #時間区分数

solution = d_time/np.power(d_division, 2)
if solution > 0.5:
    sys.exit("'Δt/Δ^2x'の値が" + str(solution) + "になり解析結果が発散します。")

#解析に必要な配列を作成
t_change = np.zeros((x_time, grids))
division = np.array(range(grids))

#t=0の時の値を計算
for i in range(len(division)):
    t_change[0][i] = np.sin(np.pi * division[i] * d_division)

#境界条件の設定, boun = 境界の値
boun = 0
for i in range(x_time):
    t_change[i][0] = boun
for i in range(len(t_change)):
    t_change[i][spase] = boun

#数値解析を行う
for _ in tqdm(range(loop), desc="proc1", ncols=80):
    for n in tqdm(range(len(t_change) - 1), desc="proc2", ncols=80, leave=False):
        for i in range(len(division) - 2):
            t_change[n+1][i+1] = t_change[n][i+1] + solution * (t_change[n][i+2] - 2 * t_change[n][i+1] + t_change[n][i])

#データの処理を行い、csvに保存
t_change = np.round(t_change, 3)
np.savetxt('out.csv', t_change, delimiter=',')

#解析結果をコンソールに表示
#print(t_change)
#print(division)

#解析結果をグラフで表示
X, Y = np.mgrid[0:x_time, 0:grids]
X = X * d_time
Y = np.round(Y * d_division, 3)

fig = plt.figure(figsize=(9, 9), facecolor="w")
ax = fig.add_subplot(111, projection="3d")
ax.set(xlabel='時間[t]', ylabel='メッシュ区間[x]', zlabel='温度[℃]')

surf = ax.plot_surface(X, Y, t_change, antialiased=False)

plt.show()