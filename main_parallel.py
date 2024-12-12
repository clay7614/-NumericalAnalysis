import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import japanize_matplotlib
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# ユーザーが与える変数
spase = 6  # メッシュ数
time = 1  # 時間区分数
d_time = 0.01  # 時間変化量
loop = 100  # 計算の反復回数
ppv = 1 # 物性値

# 自動的に算出する変数
d_division = 1.0 / spase  # メッシュ間変化量
grids = spase + 1  # 1格子数
x_time = int(time / d_time)  # 時間区分数

solution = d_time / np.power(d_division, 2)
if solution > 0.5:
    sys.exit("'Δt/Δ^2x'の値が" + str(solution) + "になり解析結果が発散します。")

# 解析に必要な配列を作成
t_change = np.zeros((x_time, grids))
division = np.array(range(grids))

# t=0の時の各メッシュの値を計算
for i in range(len(division)):
    t_change[0][i] = 20 * np.sin(np.pi * division[i] * d_division)

# 境界条件の設定, boun = 境界の値
boun = 0
for i in range(x_time):
    t_change[i][0] = boun
for i in range(len(t_change)):
    t_change[i][spase] = boun

# 並列計算用の関数
def update_time_step(args):
    n, t_current, t_next = args
    for i in range(1, len(t_current) - 1):
        t_next[i] = t_current[i] + solution * ppv * (t_current[i + 1] - 2 * t_current[i] + t_current[i - 1])

# 数値解析を行う
for _ in tqdm(range(loop), desc="proc1", ncols=80):
    with ThreadPoolExecutor() as executor:
        for n in tqdm(range(len(t_change) - 1), desc="proc2", ncols=80, leave=False):
            executor.submit(update_time_step, (n, t_change[n], t_change[n + 1]))

# データの処理を行い、csvに保存
t_change = np.round(t_change, 3)
np.savetxt('out.csv', t_change, delimiter=',')

#解析結果をグラフで表示
"""
X, Y = np.mgrid[0:x_time, 0:grids]
X = X * d_time
Y = np.round(Y * d_division, 3)
print(Y)

fig = plt.figure(figsize=(9, 9), facecolor="w")
ax = fig.add_subplot(111, projection="3d")
ax.set(xlabel='時間[t]', ylabel='メッシュ区間[x]', zlabel='温度[℃]')

surf = ax.plot_surface(X, Y, t_change, antialiased=False)

plt.show()
"""

#解析結果を二次元アニメーションで表示
fig = plt.figure()
ims = []

for i in range(x_time):
    rand = t_change[i]
    img = plt.plot(rand) # グラフを作成
    plt.title("sample animation")
    plt.ylim(0,30)

    ims.append(img) # グラフを配列に追加
    plt.xlabel("メッシュ")
    plt.ylabel("温度[℃]")


# 100枚のプロットを 100ms ごとに表示するアニメーション
ani = animation.ArtistAnimation(fig, ims, interval=10)
plt.show()
