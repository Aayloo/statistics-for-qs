# 生成 04_backtest_rigor 模块配图（assets/*.png）
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
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


rng = np.random.default_rng(1)

# 1) IC t 统计与 p 值
T, mu_ic, sd_ic = 60, 0.04, 0.12
t_obs = mu_ic * np.sqrt(T) / sd_ic
t_null = rng.normal(0, 1, 20000)  # H0 下 t ~ N(0,1) 近似
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(t_null, bins=60, density=True, alpha=0.6, color="#2f5597", label="H0：因子无效时的 t 分布")
ax.axvline(t_obs, color="#c0392b", lw=2)
ax.text(t_obs + 0.15, 0.36, f"观测 t = {t_obs:.2f}", color="#c0392b", fontsize=12)
x = np.linspace(t_obs, 4, 200)
ax.fill_between(x, stats.norm.pdf(x), color="#c0392b", alpha=0.4)
ax.text(2.6, 0.06, "尾部面积 = p 值", color="#c0392b", fontsize=11)
ax.set_xlabel("t 统计量")
ax.set_ylabel("密度")
ax.set_title("IC 的 t 检验：H0 下 t 分布 + 观测值 + p 值")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "ic_tstat.png")


# 2) 泄漏控制示意：purge + embargo + walk-forward
fig, axes = plt.subplots(2, 1, figsize=(11, 6.5))
colors = {"train": "#4C72B0", "test": "#2E8B57", "purge": "#C0392B", "embargo": "#E67E22"}


def draw_fold(ax, folds, title):
    ax.set_yticks([])
    for i, (start, end, kind) in enumerate(folds):
        ax.add_patch(Rectangle((start, 0), end - start, 0.7, fc=colors[kind], ec="white"))
        ax.text((start + end) / 2, 0.35, kind, ha="center", va="center", fontsize=9, color="white")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 0.9)
    ax.set_title(title, fontsize=11)
    ax.set_xticks([])


draw_fold(axes[0], [
    (0, 8, "train"), (8, 11, "purge"), (11, 16, "test"), (16, 19, "embargo"),
    (19, 30, "train"),
], "同一折内：test 前后的 purge（标签重叠）与 embargo（序列相关）")
draw_fold(axes[1], [
    (0, 6, "train"), (6, 10, "test"),
    (0, 10, "train"), (10, 14, "test"),
    (0, 14, "train"), (14, 18, "test"),
    (0, 18, "train"), (18, 22, "test"),
], "walk-forward：只用过去训练，滚动向未来测试")
fig.tight_layout()
save(fig, "leakage_walkforward.png")


# 3) CPCV：N=6, K=2 → 15 折
N, K = 6, 2
import itertools
folds = list(itertools.combinations(range(N), K))
fig, ax = plt.subplots(figsize=(9, 8))
for r, test_groups in enumerate(folds):
    for g in range(N):
        c = "#C0392B" if g in test_groups else "#4C72B0"
        ax.add_patch(Rectangle((g, len(folds) - 1 - r), 0.8, 0.8, fc=c, ec="white"))
ax.set_xlim(-0.5, N + 1.5)
ax.set_ylim(-1, len(folds) + 0.5)
ax.set_xticks(range(N))
ax.set_xticklabels([f"组 {i+1}" for i in range(N)])
ax.set_yticks([])
ax.set_xlabel("时间分组（N=6）")
ax.set_ylabel("C(6,2)=15 折")
ax.set_title("Combinatorial Purged CV：每折选 K=2 组做测试，共 15 折 → 5 条样本外路径")
ax.grid(alpha=0.1)
fig.tight_layout()
save(fig, "cpcv_matrix.png")


# 4) DSR：多重试验把"最大夏普"推高
n_trials = 1000
sr_single = rng.normal(0, 1 / np.sqrt(252), 20000)
sr_max = np.array([rng.normal(0, 1 / np.sqrt(252), n_trials).max() for _ in range(2000)])
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(sr_single, bins=80, density=True, alpha=0.55, color="#4C72B0", label="单次试验的夏普（年化）")
ax.hist(sr_max, bins=80, density=True, alpha=0.55, color="#C0392B", label="1000 次试验的最大夏普")
ax.axvline(2.0, color="#2F5597", lw=1.8, ls="--")
ax.text(2.05, 4.0, "观测 SR=2.0", fontsize=11, color="#2F5597")
ax.set_xlabel("年化夏普")
ax.set_ylabel("密度")
ax.set_title("测 1000 个策略后，最大夏普的基准被抬高 → 需要 DSR 校正")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "dsr_deflation.png")


# 5) PBO：样本内排名 vs 样本外表现
is_perf = rng.normal(0, 1, 30)
oos_perf = 0.3 * is_perf + rng.normal(0, 1, 30)
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(is_perf, oos_perf, s=30, color="#4C72B0", alpha=0.75)
winner = np.argmax(is_perf)
ax.scatter(is_perf[winner], oos_perf[winner], s=120, facecolors="none", edgecolors="#C0392B", lw=2)
ax.annotate("样本内最优\n样本外平平", xy=(is_perf[winner], oos_perf[winner]),
            xytext=(is_perf[winner] - 1.5, oos_perf[winner] + 0.8), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#C0392B"))
ax.axhline(np.median(oos_perf), color="0.4", ls=":", lw=1)
ax.set_xlabel("样本内表现（排名用）")
ax.set_ylabel("样本外表现")
ax.set_title("CSCV 核心观察：样本内赢家样本外未必赢（PBO 度量这种翻转频率）")
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "pbo_rank.png")


# 6) 因子 zoo：t 值分布（数据挖掘筛选后的右移）
t_all = rng.normal(0, 1, 20000)
t_published = np.concatenate([rng.normal(0, 1, 15000), rng.normal(3, 0.8, 5000)])
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(t_all, bins=60, density=True, alpha=0.55, color="#4C72B0", label="全部被测试因子的 t 值")
ax.hist(t_published, bins=60, density=True, alpha=0.55, color="#C9A227", label="被「发表」的因子 t 值")
ax.axvline(2, color="#C0392B", ls="--", lw=1.5)
ax.axvline(3, color="#2F5597", ls="--", lw=1.5)
ax.text(2.05, 0.30, "t=2（传统显著）", color="#C0392B", fontsize=10)
ax.text(3.05, 0.24, "t=3（Harvey-Liu）", color="#2F5597", fontsize=10)
ax.set_xlabel("t 统计量")
ax.set_ylabel("密度")
ax.set_title("因子动物园：被筛选过的 t 值整体右移 → 阈值应提高到 3")
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()
save(fig, "factor_zoo.png")
