# 生成 03_time_series 模块配图（assets/*.png）
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


rng = np.random.default_rng(0)
N = 500

# 1) 平稳 vs 随机游走 vs 趋势
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
wn = rng.normal(0, 1, N)
rw = np.cumsum(rng.normal(0, 1, N))
trend = 0.02 * np.arange(N) + rng.normal(0, 1, N)
for ax, y, t, c in zip(axes, (wn, rw, trend),
                       ("白噪声（平稳）", "随机游走（单位根，非平稳）", "确定性趋势 + 噪声"),
                       ("#2f5597", "#c0392b", "#1e8449")):
    ax.plot(y, lw=0.9, color=c)
    ax.set_title(t, fontsize=11)
    ax.grid(alpha=0.2)
axes[0].set_ylabel("X_t")
fig.suptitle("三类序列：均值/方差是否随时间变化", fontsize=13)
fig.tight_layout()
save(fig, "stationarity.png")


def acf(x, maxlag=30):
    x = x - x.mean()
    v = np.array([np.corrcoef(x[:-l], x[l:])[0, 1] if l > 0 else 1.0 for l in range(maxlag + 1)])
    return v


# 2) ACF 对比
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
ar = np.zeros(N)
for t in range(1, N):
    ar[t] = 0.8 * ar[t - 1] + rng.normal(0, 1)
series = [
    ("白噪声：ACF 全部不显著", wn),
    ("AR(1) φ=0.8：ACF 指数衰减", ar),
    ("随机游走：ACF 缓慢衰减（非平稳）", rw),
]
lags = np.arange(31)
for ax, (t, y) in zip(axes, series):
    a = acf(y)
    ax.vlines(lags, 0, a, color="#2f5597", lw=1.4)
    ax.plot(lags, a, "o", ms=3, color="#2f5597")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.axhline(1.96 / np.sqrt(N), color="#c0392b", ls="--", lw=1)
    ax.axhline(-1.96 / np.sqrt(N), color="#c0392b", ls="--", lw=1)
    ax.set_title(t, fontsize=11)
    ax.grid(alpha=0.2)
axes[2].set_xlabel("滞后 k")
fig.suptitle("ACF：白噪声快速截断，非平稳缓慢衰减", fontsize=13)
fig.tight_layout()
save(fig, "acf_plots.png")


# 3) 协整
beta = 0.7
s = rng.normal(0, 0.5, N)
common = np.cumsum(rng.normal(0, 1, N))
y1 = common + s
y2 = beta * common + rng.normal(0, 0.5, N)
spread = y1 - y2 / beta
fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
axes[0].plot(y1, lw=1, color="#2f5597", label="y1")
axes[0].plot(y2, lw=1, color="#c9a227", label="y2")
axes[0].set_title("两个非平稳序列，但长期保持固定关系（协整）")
axes[0].legend()
axes[0].grid(alpha=0.2)
z = (spread - spread.mean()) / spread.std()
axes[1].plot(z, lw=1, color="#1e8449")
axes[1].axhline(0, color="0.4", lw=0.8)
axes[1].axhline(2, color="#c0392b", ls="--", lw=1)
axes[1].axhline(-2, color="#c0392b", ls="--", lw=1)
axes[1].set_title("价差 z-score：均值回复 → 配对交易机会")
axes[1].grid(alpha=0.2)
fig.tight_layout()
save(fig, "cointegration.png")


# 4) GARCH 波动率聚集
omega, alpha, bbeta = 0.01, 0.1, 0.85
sigma2 = np.zeros(N)
rets = np.zeros(N)
sigma2[0] = 1
for t in range(1, N):
    sigma2[t] = omega + alpha * rets[t - 1] ** 2 + bbeta * sigma2[t - 1]
    rets[t] = np.sqrt(sigma2[t]) * rng.normal()
fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
axes[0].plot(rets, lw=0.7, color="#2f5597")
axes[0].set_title("收益：大波动聚集（volatility clustering）")
axes[0].grid(alpha=0.2)
axes[1].plot(np.sqrt(sigma2), lw=1.2, color="#c0392b")
axes[1].set_title("GARCH(1,1) 条件波动率：ω=0.01, α=0.1, β=0.85")
axes[1].grid(alpha=0.2)
fig.tight_layout()
save(fig, "garch.png")


# 5) 两 regime 模拟
regime = rng.choice([0, 1], size=N, p=[0.7, 0.3])
vols = np.array([0.5, 2.0])
rets2 = rng.normal(0, vols[regime])
fig, ax = plt.subplots(figsize=(10, 4.5))
colors = ["#2f5597", "#c0392b"]
for r in (0, 1):
    idx = np.where(regime == r)[0]
    ax.scatter(idx, rets2[idx], s=6, color=colors[r], alpha=0.6, label=f"regime {r}（σ={vols[r]}）")
ax.set_title("隐藏状态切换：低波动 / 高波动两个 regime")
ax.set_xlabel("t")
ax.legend()
ax.grid(alpha=0.2)
fig.tight_layout()
save(fig, "regimes.png")
