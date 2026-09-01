# 生成 01_probability 模块配图（assets/*.png）
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


# 1) 连续分布
fig, axes = plt.subplots(2, 3, figsize=(13, 7))
x = np.linspace(-5, 5, 500)
axes[0, 0].plot(x, stats.norm.pdf(x), label="N(0,1)")
axes[0, 0].plot(x, stats.norm.pdf(x, 0, 2), label="N(0,2)")
axes[0, 0].plot(x, stats.t.pdf(x, 5), label="t(5)")
axes[0, 0].plot(x, stats.cauchy.pdf(x), label="Cauchy", lw=1.2)
axes[0, 0].set_title("正态 vs t vs 柯西（肥尾）")
axes[0, 0].legend()

x = np.linspace(0, 25, 400)
for k in (2, 5, 10):
    axes[0, 1].plot(x, stats.chi2.pdf(x, k), label=f"χ²(k={k})")
axes[0, 1].set_title("卡方分布（方差检验）")
axes[0, 1].legend()

x = np.linspace(0, 5, 400)
for d1, d2 in ((5, 10), (2, 5)):
    axes[0, 2].plot(x, stats.f.pdf(x, d1, d2), label=f"F({d1},{d2})")
axes[0, 2].set_title("F 分布（回归显著性）")
axes[0, 2].legend()

x = np.linspace(0, 6, 400)
for lam in (0.5, 1, 2):
    axes[1, 0].plot(x, stats.expon.pdf(x, scale=1 / lam), label=f"Exp(λ={lam})")
axes[1, 0].set_title("指数分布（等待时间，无记忆性）")
axes[1, 0].legend()

x = np.linspace(0, 6, 500)
for s in (0.3, 0.7, 1.2):
    axes[1, 1].plot(x, stats.lognorm.pdf(x, s), label=f"LogN(σ={s})")
axes[1, 1].set_title("对数正态（价格/资产价值）")
axes[1, 1].legend()

x = np.linspace(-3, 3, 400)
axes[1, 2].plot(x, stats.uniform.pdf(x, -2, 4), label="U(-2,2)")
axes[1, 2].plot(x, stats.uniform.pdf(x, 0, 1), label="U(0,1)")
axes[1, 2].set_title("均匀分布（无信息先验）")
axes[1, 2].legend()

for ax in axes.flat:
    ax.grid(alpha=0.25)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
fig.tight_layout()
save(fig, "continuous_dists.png")


# 2) 离散分布
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
k = np.arange(0, 31)
for n, p in ((10, 0.3), (10, 0.5), (30, 0.5)):
    axes[0, 0].plot(k, stats.binom.pmf(k, n, p), "o-", label=f"Bin({n},{p})")
axes[0, 0].set_title("二项分布（n 次独立试验成功数）")
axes[0, 0].legend()

for lam in (1, 4, 10):
    axes[0, 1].plot(k, stats.poisson.pmf(k, lam), "o-", label=f"Pois(λ={lam})")
axes[0, 1].set_title("泊松分布（稀有事件计数）")
axes[0, 1].legend()

k = np.arange(1, 11)
for p in (0.3, 0.5):
    axes[1, 0].plot(k, stats.geom.pmf(k, p), "o-", label=f"Geom(p={p})")
axes[1, 0].set_title("几何分布（首次成功所需次数）")
axes[1, 0].legend()

axes[1, 1].plot(k, stats.binom.pmf(k, 30, 0.5), "o-", label="Bin(30,0.5)")
x = np.linspace(0, 30, 300)
axes[1, 1].plot(x, stats.norm.pdf(x, 15, np.sqrt(7.5)), label="N(15,7.5)")
axes[1, 1].set_title("二项 → 正态近似（CLT 的离散版本）")
axes[1, 1].legend()

for ax in axes.flat:
    ax.grid(alpha=0.25)
    ax.set_xlabel("k")
    ax.set_ylabel("P(X=k)")
fig.tight_layout()
save(fig, "discrete_dists.png")


# 3) CLT 收敛（均匀分布样本均值）
rng = np.random.default_rng(0)
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, n in zip(axes.flat, (1, 5, 30, 100)):
    means = rng.uniform(0, 1, size=(20000, n)).mean(axis=1)
    ax.hist(means, bins=60, density=True, alpha=0.65, color="#4C72B0")
    x = np.linspace(0, 1, 300)
    sd = np.sqrt((1 / 12) / n)
    ax.plot(x, stats.norm.pdf(x, 0.5, sd), "r-", lw=1.6, label="正态近似")
    ax.set_title(f"n = {n}（样本均值分布）")
    ax.legend()
    ax.grid(alpha=0.25)
fig.suptitle("中心极限定理：均匀分布的样本均值 → 正态", fontsize=13)
fig.tight_layout()
save(fig, "clt_convergence.png")


# 4) 贝叶斯树（疾病检测）
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.axis("off")


def node(x, y, text, color="#dbe9f6", ec="#2f5597"):
    ax.add_patch(plt.Rectangle((x - 0.22, y - 0.055), 0.44, 0.11, fc=color, ec=ec, lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5)


def edge(x1, y1, x2, y2, label, color="0.4"):
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.2)
    ax.text((x1 + x2) / 2 + 0.04, (y1 + y2) / 2, label, fontsize=9, color=color)


node(0, 0.5, "随机一人", "#ffe9c7", "#b5711f")
edge(0, 0.44, -0.55, 0.12, "患病 P=0.01", "#c0392b")
edge(0, 0.44, 0.55, 0.12, "健康 P=0.99", "#1e8449")
node(-0.55, 0, "患病")
node(0.55, 0, "健康")
edge(-0.55, -0.06, -0.82, -0.38, "阳性 0.99", "#c0392b")
edge(-0.55, -0.06, -0.28, -0.38, "阴性 0.01", "0.5")
edge(0.55, -0.06, 0.28, -0.38, "阳性 0.01", "#c0392b")
edge(0.55, -0.06, 0.82, -0.38, "阴性 0.99", "0.5")
node(-0.82, -0.5, "阳性∩患病\n= 0.0099", "#fadbd8", "#a93226")
node(-0.28, -0.5, "阴性∩患病\n= 0.0001", "#d5f5e3", "#1e8449")
node(0.28, -0.5, "阳性∩健康\n= 0.0099", "#fadbd8", "#a93226")
node(0.82, -0.5, "阴性∩健康\n= 0.9801", "#d5f5e3", "#1e8449")
ax.text(
    0,
    -0.72,
    "P(患病|阳性) = 0.0099 / (0.0099+0.0099) ≈ 50%",
    ha="center",
    fontsize=11,
    color="#a93226",
)
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-0.85, 0.62)
save(fig, "bayes_tree.png")


# 5) 次序统计量：n 个均匀随机变量的最大值期望
fig, ax = plt.subplots(figsize=(7.5, 5))
n = np.arange(1, 21)
ax.plot(n, n / (n + 1), "o-", label="理论 E[max] = n/(n+1)")
sim = [rng.uniform(0, 1, size=(5000, i)).max(axis=1).mean() for i in n]
ax.plot(n, sim, "s--", label="模拟均值", alpha=0.8)
ax.set_xlabel("n（均匀随机变量的个数）")
ax.set_ylabel("E[max]")
ax.set_title("次序统计量：最大值的期望")
ax.grid(alpha=0.25)
ax.legend()
save(fig, "order_stats.png")


# 6) 赌徒破产：随机游走 + 破产概率
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
N, i0, barrier = 10, 5, 10
for _ in range(15):
    pos = i0
    path = [pos]
    while 0 < pos < barrier and len(path) < 300:
        pos += rng.choice([-1, 1])
        path.append(pos)
    axes[0].plot(path, lw=0.8, alpha=0.75)
axes[0].axhline(barrier, color="#c0392b", lw=1.4, ls="--")
axes[0].axhline(0, color="#1e8449", lw=1.4, ls="--")
axes[0].text(1, barrier + 0.4, f"赢光 {barrier}", color="#c0392b")
axes[0].text(1, 0.4, "破产 0", color="#1e8449")
axes[0].set_title("对称随机游走路径（吸收壁 0 与 10）")
axes[0].set_xlabel("步数")
axes[0].set_ylabel("资金")
axes[0].grid(alpha=0.25)

p = np.linspace(0.001, 0.999, 300)
axes[1].axhline(1 - i0 / barrier, color="#c0392b", ls="--", label="公平 p=0.5：P(破产)=1−i/N=0.5")
q = 1 - p
ruin_bias = ((q / p) ** barrier - (q / p) ** i0) / ((q / p) ** barrier - 1)
axes[1].plot(p, ruin_bias, label="有偏游戏 P(破产)（解析解）")
axes[1].set_title("赌徒破产概率（起始 5，目标 10）")
axes[1].set_xlabel("单局胜率 p")
axes[1].set_ylabel("P(破产)")
axes[1].set_ylim(0, 1.02)
axes[1].grid(alpha=0.25)
axes[1].legend()
fig.tight_layout()
save(fig, "gamblers_ruin.png")


# 7) PDF 与 CDF（正态）
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
x = np.linspace(-4, 4, 600)
pdf = stats.norm.pdf(x)
axes[0].plot(x, pdf, lw=1.8, color="#2f5597")
axes[0].fill_between(x, pdf, where=(x >= -1) & (x <= 1), color="#c9a227", alpha=0.55)
axes[0].set_title("P(−1 ≤ X ≤ 1) = 阴影面积 ≈ 68.3%")
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].grid(alpha=0.25)
cdf = stats.norm.cdf(x)
axes[1].plot(x, cdf, lw=1.8, color="#2f5597")
for v in (-1, 1):
    axes[1].axvline(v, color="#c0392b", ls="--", lw=1)
axes[1].axhline(stats.norm.cdf(-1), color="#1e8449", ls=":", lw=1)
axes[1].axhline(stats.norm.cdf(1), color="#1e8449", ls=":", lw=1)
axes[1].set_title("CDF：F(x) = P(X ≤ x)，F(1)−F(−1) = 0.683")
axes[1].set_xlabel("x")
axes[1].set_ylabel("F(x)")
axes[1].grid(alpha=0.25)
fig.tight_layout()
save(fig, "pdf_cdf.png")


# 8) 正态 68-95-99.7
fig, ax = plt.subplots(figsize=(9, 5))
x = np.linspace(-4, 4, 800)
pdf = stats.norm.pdf(x)
ax.plot(x, pdf, lw=1.8, color="#2f5597")
for k, c, label in ((1, "#c9a227", "68.3%"), (2, "#e67e22", "95.4%"), (3, "#c0392b", "99.7%")):
    ax.fill_between(x, pdf, where=(x >= -k) & (x <= k), color=c, alpha=0.35)
    ax.text(k + 0.08, stats.norm.pdf(0) * 0.55 - k * 0.02, f"±{k}σ  {label}", fontsize=11)
ax.set_title("正态分布：68-95-99.7 法则")
ax.set_xlabel("x（单位：σ）")
ax.set_ylabel("f(x)")
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "normal_areas.png")


# 9) 指数分布无记忆性
fig, ax = plt.subplots(figsize=(9, 5))
t = np.linspace(0, 7, 500)
lam = 0.8
s = 2.0
h = 2.0
ax.plot(t, np.exp(-lam * t), lw=2, color="#2f5597", label="生存函数 S(t)=P(X>t)=e^(−λt)")
ax.fill_between(t, 0, np.exp(-lam * t), where=(t >= s + h), color="#c0392b", alpha=0.4)
ax.axvspan(s + h, 7, color="#c0392b", alpha=0.12)
ax.axvline(s, color="#1e8449", ls="--", lw=1)
ax.axvline(s + h, color="#1e8449", ls="--", lw=1)
ax.annotate(
    "红色面积 = P(X > s+h)",
    xy=(s + h + 0.3, np.exp(-lam * (s + h)) / 2),
    fontsize=10,
    color="#c0392b",
)
ax.text(3.8, 0.9, "P(X>s+h | X>s) = P(X>h)\n（已存活 s 后，剩余寿命分布不变）", fontsize=10.5)
ax.set_xlabel("t")
ax.set_ylabel("P(X > t)")
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.25)
ax.legend(loc="upper right")
fig.tight_layout()
save(fig, "memoryless.png")


# 10) 相关系数散点（教学用）
fig, axes = plt.subplots(2, 2, figsize=(11, 9))
rng = np.random.default_rng(2)
for ax, rho in zip(axes.flat, (0.9, 0.5, 0.0, -0.8)):
    z1, z2 = rng.normal(size=(2000, 2)).T
    x = z1
    y = rho * z1 + np.sqrt(1 - rho**2) * z2
    ax.scatter(x, y, s=3, alpha=0.35, color="#2f5597")
    ax.set_title(f"ρ = {rho:+.1f}")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(alpha=0.2)
fig.suptitle("相关系数 ρ 的直观：线性关系的方向与强度（ρ=0 不代表独立）", fontsize=13)
fig.tight_layout()
save(fig, "correlation_scatter.png")
