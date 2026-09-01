# 生成 02_inference 模块配图（assets/*.png）
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


# 1) MLE：对数似然最大化
rng = np.random.default_rng(0)
data = np.array([10.1, 9.7, 10.4, 10.2, 9.9, 10.3, 9.8, 10.0])
mu = np.linspace(9.4, 10.6, 400)
ll = -0.5 * np.sum((data[:, None] - mu) ** 2, axis=0)  # sigma=1 已知
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.plot(mu, ll, lw=2, color="#2f5597")
mu_hat = data.mean()
ax.axvline(mu_hat, color="#c0392b", ls="--", lw=1.4)
ax.plot(mu_hat, ll.max(), "o", color="#c0392b")
ax.annotate(f"MLE = 样本均值 = {mu_hat:.2f}", xy=(mu_hat, ll.max()), xytext=(mu_hat + 0.08, ll.max() - 0.5),
            arrowprops=dict(arrowstyle="->", color="#c0392b"), fontsize=11, color="#c0392b")
ax.set_xlabel("μ（正态均值候选）")
ax.set_ylabel("对数似然 ℓ(μ)")
ax.set_title("极大似然估计：让观测数据最「可能」的 μ")
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "mle.png")


# 2) t 分布 vs 正态
fig, ax = plt.subplots(figsize=(8.5, 5))
x = np.linspace(-4, 4, 600)
ax.plot(x, stats.norm.pdf(x), lw=2, color="#2f5597", label="N(0,1)")
for df in (3, 10, 30):
    ax.plot(x, stats.t.pdf(x, df), lw=1.4, ls="--", label=f"t(df={df})")
ax.set_xlabel("x")
ax.set_ylabel("密度")
ax.set_title("t 分布：自由度越小尾部越厚（小样本方差未知时的修正）")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()
save(fig, "t_vs_normal.png")


# 3) 功效曲线（单样本 t 检验）
fig, ax = plt.subplots(figsize=(8.5, 5))
n = np.arange(5, 121)
alpha = 0.05
for d in (0.2, 0.5, 0.8):
    tcrit = stats.t.ppf(1 - alpha / 2, n - 1)
    nc = d * np.sqrt(n)
    power = 1 - stats.nct.cdf(tcrit, n - 1, nc) + stats.nct.cdf(-tcrit, n - 1, nc)
    ax.plot(n, power, lw=1.8, label=f"效应量 d = {d}")
ax.axhline(0.8, color="#c0392b", ls=":", lw=1.2)
ax.text(5, 0.815, "80% 功效（常用标准）", color="#c0392b", fontsize=10)
ax.set_xlabel("样本量 n")
ax.set_ylabel("检验功效")
ax.set_title("功效随样本量上升：效应越小，需要的样本越大")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()
save(fig, "power_curve.png")


# 4) p 值分布与多重检验
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
p0 = rng.uniform(0, 1, 20000)
z1 = rng.normal(0.5, 1, 20000)
p1 = 2 * (1 - stats.norm.cdf(np.abs(z1)))
axes[0].hist(p0, bins=40, density=True, alpha=0.6, label="H0 为真（均匀）", color="#2f5597")
axes[0].hist(p1, bins=40, density=True, alpha=0.6, label="H1 为真（偏小）", color="#c9a227")
axes[0].axvline(0.05, color="#c0392b", ls="--", lw=1.3)
axes[0].text(0.052, 2.2, "α=0.05", color="#c0392b", fontsize=11)
axes[0].set_xlabel("p 值")
axes[0].set_ylabel("密度")
axes[0].set_title("H0 下 p 值均匀分布：5% 的假阳性不可避免")
axes[0].legend()

counts = rng.binomial(1000, 0.05, 20000)
axes[1].hist(counts, bins=45, density=True, alpha=0.7, color="#2f5597")
axes[1].axvline(50, color="#c0392b", ls="--", lw=1.3)
axes[1].text(52, 0.03, "期望 ≈ 50 个假阳性", color="#c0392b", fontsize=11)
axes[1].set_xlabel("显著个数（1000 次检验）")
axes[1].set_ylabel("密度")
axes[1].set_title("全部是噪声时，1000 次检验仍会「发现」约 50 个显著")
axes[1].grid(alpha=0.25)
fig.tight_layout()
save(fig, "pvalue_dist.png")


# 5) OLS 假设诊断（4 面板）
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
xr = np.linspace(0, 2, 80)
y_lin = 1 + 0.8 * xr + rng.normal(0, 0.15, 80)
axes[0, 0].scatter(xr, y_lin, s=8, color="#2f5597", alpha=0.7)
axes[0, 0].plot(xr, 1 + 0.8 * xr, color="#c0392b", lw=1.6)
axes[0, 0].set_title("① 线性：均值是直线")

y_cone = rng.normal(0, 0.15 * (1 + xr))
axes[0, 1].scatter(xr, y_cone, s=8, color="#2f5597", alpha=0.7)
axes[0, 1].axhline(0, color="#c0392b", lw=1.2)
axes[0, 1].set_title("② 同方差：残差散度不随 x 变化（此处违反）")

resid = rng.normal(0, 0.2, 300)
stats.probplot(resid, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title("③ 正态性：QQ 图近似直线")

t = np.arange(80)
y_ar = np.zeros(80)
for i in range(1, 80):
    y_ar[i] = 0.85 * y_ar[i - 1] + rng.normal(0, 0.25)
axes[1, 1].plot(t, y_ar, lw=1.2, color="#2f5597")
axes[1, 1].set_title("④ 独立：残差不应有序列相关（此处违反）")
axes[1, 1].grid(alpha=0.25)

for ax in axes.flat:
    ax.grid(alpha=0.2)
fig.suptitle("OLS 四大假设：回归推断成立的前提", fontsize=13)
fig.tight_layout()
save(fig, "ols_assumptions.png")
