# 生成 05_bayesian 模块配图（assets/*.png）
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


rng = np.random.default_rng(3)

# 1) Beta-Binomial：先验 → 后验
x = np.linspace(0, 1, 500)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x, stats.beta.pdf(x, 2, 2), lw=2, color="#4C72B0", label="先验 Beta(2,2)（无信息）")
ax.plot(x, stats.beta.pdf(x, 6, 4), lw=2, ls="--", color="#C9A227", label="中间 Beta(6,4)（4正2反后）")
ax.plot(x, stats.beta.pdf(x, 10, 4), lw=2, ls="-.", color="#C0392B", label="后验 Beta(10,4)（8正2反后）")
ax.set_xlabel("θ（成功率）")
ax.set_ylabel("密度")
ax.set_title("Beta-Binomial 共轭：数据越多，后验越尖")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "beta_binomial.png")


# 2) Normal-Normal 后验收缩
x = np.linspace(-2, 3, 500)
prior = stats.norm.pdf(x, 0, 1)
lik = stats.norm.pdf(x, 1.2, 0.5)
post_prec = 1 / 1 + 1 / 0.5**2
post_mean = (0 / 1 + 1.2 / 0.25) / post_prec
post = stats.norm.pdf(x, post_mean, np.sqrt(1 / post_prec))
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x, prior, lw=2, color="#4C72B0", label="先验 N(0,1)")
ax.plot(x, lik, lw=2, color="#C9A227", label="似然（数据均值 1.2，SE 0.5）")
ax.plot(x, post, lw=2.4, color="#C0392B", label=f"后验 N({post_mean:.2f}, σ²)")
ax.set_xlabel("θ")
ax.set_ylabel("密度")
ax.set_title("Normal-Normal：后验 = 先验与似然的精度加权平均（收缩）")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "posterior_shrinkage.png")


# 3) MCMC 轨迹（随机游走 Metropolis 示意）
def mh(n=3000, chain=0):
    draws = np.zeros(n)
    cur = 0.0
    acc = 0
    for i in range(n):
        prop = cur + rng.normal(0, 0.8)
        lp_cur = stats.norm.logpdf(cur, 0.8, 1)
        lp_prop = stats.norm.logpdf(prop, 0.8, 1)
        if np.log(rng.uniform()) < lp_prop - lp_cur:
            cur = prop
            acc += 1
        draws[i] = cur
    return draws


chains = [mh(1500, c) for c in range(3)]
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for c, col in zip(chains, ("#4C72B0", "#C9A227", "#C0392B")):
    axes[0].plot(c, lw=0.7, alpha=0.8, color=col)
axes[0].axvline(500, color="0.3", ls="--", lw=1)
axes[0].text(520, 2.6, "burn-in", fontsize=10)
axes[0].set_xlabel("迭代")
axes[0].set_ylabel("θ")
axes[0].set_title("MCMC 轨迹：收敛后围绕后验均值波动")
axes[0].grid(alpha=0.2)
post_draws = np.concatenate([c[500:] for c in chains])
axes[1].hist(post_draws, bins=60, density=True, alpha=0.65, color="#2f5597")
xx = np.linspace(-2, 3.5, 300)
axes[1].plot(xx, stats.norm.pdf(xx, 0.8, 1), color="#C0392B", lw=2, label="真实后验 N(0.8,1)")
axes[1].set_xlabel("θ")
axes[1].set_ylabel("密度")
axes[1].set_title("后验直方图（burn-in 之后）")
axes[1].legend()
axes[1].grid(alpha=0.2)
fig.tight_layout()
save(fig, "mcmc_trace.png")


# 4) 贝叶斯 regime 后验（示意）
N = 300
regime = np.zeros(N)
for t in range(1, N):
    regime[t] = 1 if rng.uniform() < 0.03 else regime[t - 1]
vols = np.array([0.5, 2.0])
rets = rng.normal(0, vols[regime.astype(int)])
lr = np.where(rets > 0, 1.0, 0.0)
post_hi = np.zeros(N)
prob = 0.3
for t in range(N):
    p_low = stats.norm.pdf(rets[t], 0, vols[0])
    p_hi = stats.norm.pdf(rets[t], 0, vols[1])
    prob = (p_hi * prob) / (p_hi * prob + p_low * (1 - prob))
    prob = 0.9 * prob + 0.1 * 0.3
    post_hi[t] = prob
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axes[0].scatter(np.arange(N), rets, s=4, c=["#C0392B" if r else "#4C72B0" for r in regime], alpha=0.6)
axes[0].set_title("收益（红色 = 高波动 regime）")
axes[0].grid(alpha=0.2)
axes[1].plot(post_hi, lw=1.5, color="#C9A227")
axes[1].fill_between(np.arange(N), post_hi, alpha=0.3, color="#C9A227")
axes[1].axhline(0.5, color="0.4", ls="--", lw=1)
axes[1].set_title("贝叶斯后验 P(高波动 regime)：数据驱动地切换")
axes[1].set_xlabel("t")
axes[1].set_ylim(0, 1.05)
axes[1].grid(alpha=0.2)
fig.tight_layout()
save(fig, "regime_posterior.png")
