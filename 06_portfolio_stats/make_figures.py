# 生成 06_portfolio_stats 模块配图（assets/*.png）
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


rng = np.random.default_rng(4)

# 1) 协方差收缩：估计误差 vs 收缩强度
p, T = 30, 60
true = np.zeros((p, p))
for i in range(p):
    for j in range(p):
        true[i, j] = 0.7 ** abs(i - j)
X = rng.multivariate_normal(np.zeros(p), true, size=T)
S = np.cov(X.T)
F = np.diag(np.diag(S))
deltas = np.linspace(0, 1, 200)
err = [np.linalg.norm(d * F + (1 - d) * S - true, "fro") for d in deltas]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(deltas, err, lw=2, color="#2F5597")
i_opt = int(np.argmin(err))
ax.plot(deltas[i_opt], err[i_opt], "o", color="#C0392B")
ax.annotate(f"最优收缩 δ={deltas[i_opt]:.2f}", xy=(deltas[i_opt], err[i_opt]),
            xytext=(deltas[i_opt] + 0.1, err[i_opt] + 0.8), fontsize=11, color="#C0392B",
            arrowprops=dict(arrowstyle="->", color="#C0392B"))
ax.set_xlabel("收缩强度 δ（0=纯样本，1=纯结构化）")
ax.set_ylabel("估计误差（Frobenius）")
ax.set_title("协方差收缩：n≈p 时纯样本误差大，适度收缩明显改善")
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "covariance_shrinkage.png")


# 2) VaR / CVaR
fig, ax = plt.subplots(figsize=(9, 5))
x = np.linspace(-0.05, 0.05, 500)
pdf = stats.norm.pdf(x, 0, 0.01)
ax.plot(x, pdf, lw=2, color="#2F5597")
var = stats.norm.ppf(0.05, 0, 0.01)
ax.fill_between(x, pdf, where=(x <= var), color="#C0392B", alpha=0.55, label="VaR(95%) 尾部")
mask = x <= var
tail = x[mask]
ax.fill_between(tail, pdf[mask], color="#C9A227", alpha=0.7, label="CVaR（尾部均值）")
ax.axvline(var, color="#C0392B", lw=1.5, ls="--")
cvar = 0.01 * stats.norm.pdf(stats.norm.ppf(0.05)) / 0.05
ax.axvline(-cvar, color="#C9A227", lw=1.5, ls="--")
ax.text(var - 0.003, 36, f"VaR = {var*100:.2f}%", color="#C0392B", fontsize=11)
ax.text(-cvar + 0.0015, 33, f"CVaR ≈ -{cvar*100:.2f}%", color="#B8860B", fontsize=11)
ax.set_xlabel("日收益")
ax.set_ylabel("密度")
ax.set_title("VaR(95%) = 5% 分位；CVaR = 尾部期望（更保守）")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "var_cvar.png")


# 3) 回撤
rets = rng.normal(0.0005, 0.01, 600)
equity = np.cumprod(1 + rets)
peak = np.maximum.accumulate(equity)
dd = (equity - peak) / peak
fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
axes[0].plot(equity, lw=1.2, color="#2F5597")
axes[0].plot(peak, lw=0.9, ls="--", color="0.5")
axes[0].set_title("净值曲线与历史峰值")
axes[0].grid(alpha=0.2)
axes[1].fill_between(np.arange(len(dd)), dd * 100, 0, color="#C0392B", alpha=0.6)
axes[1].set_title("回撤（%）：最大回撤 = 最深谷")
axes[1].set_xlabel("t")
axes[1].grid(alpha=0.2)
fig.tight_layout()
save(fig, "drawdown.png")


# 4) Kelly
p, b = 0.55, 1.0
f = np.linspace(0, 0.999, 300)
g = p * np.log(1 + b * f) + (1 - p) * np.log(1 - f)
f_star = p - (1 - p) / b
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(f, g, lw=2, color="#2F5597")
ax.axvline(f_star, color="#C0392B", ls="--", lw=1.5)
ax.axhline(0, color="0.4", lw=0.8)
ax.plot(f_star, g.max(), "o", color="#C0392B")
ax.annotate(f"Kelly f* = {f_star:.2f}", xy=(f_star, g.max()), xytext=(f_star + 0.08, g.max() - 0.01),
            fontsize=11, color="#C0392B", arrowprops=dict(arrowstyle="->", color="#C0392B"))
ax.set_xlabel("下注比例 f")
ax.set_ylabel("对数增长率 g(f)")
ax.set_title("Kelly：超过 f* 后增长率反而下降（过度下注 = 毁灭）")
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "kelly.png")
