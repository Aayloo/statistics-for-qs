# 生成学习路径图（assets/path_*.png）——替代 mermaid，全站统一风格
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

STAGE_COLORS = [
    ("#4C72B0", "#DCE6F2", "面试硬基础"),
    ("#C9A227", "#FFF3CD", "核心区分度"),
    ("#2E8B57", "#E2F0E5", "差异化进阶"),
    ("#7D6BA6", "#EAE6F5", "自测"),
]


def draw(groups, title, out, note=None):
    """groups: [(阶段名, [箱体标题...], [副标题...])]"""
    fig, ax = plt.subplots(figsize=(12.5, 4.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis("off")

    ng = len(groups)
    gw = 96 / ng - 2.2
    ys = []
    xs = []
    for gi, (label, boxes, subs) in enumerate(groups):
        x0 = 1.5 + gi * (96 / ng)
        color, fill, _ = STAGE_COLORS[gi % len(STAGE_COLORS)]
        # 阶段带
        band = FancyBboxPatch((x0, 8), gw, 27, boxstyle="round,pad=0.6",
                              fc=fill, ec=color, lw=1.3, alpha=0.9)
        ax.add_patch(band)
        ax.text(x0 + gw / 2, 31.5, label, ha="center", va="center",
                fontsize=10.5, color=color, fontweight="bold")
        # 箱体
        nb = len(boxes)
        bw = min(15, (gw - 1.5) / nb)
        gap = (gw - bw * nb) / (nb + 1)
        row_xs = []
        for bi, (b, s) in enumerate(zip(boxes, subs)):
            bx = x0 + gap + bi * (bw + gap)
            by = 17.5
            box = FancyBboxPatch((bx, by), bw, 8.5, boxstyle="round,pad=0.25",
                                 fc="white", ec=color, lw=1.8)
            ax.add_patch(box)
            ax.text(bx + bw / 2, by + 5.6, b, ha="center", va="center",
                    fontsize=8.4, fontweight="bold", color="#1f2d3d")
            ax.text(bx + bw / 2, by + 2.6, s, ha="center", va="center",
                    fontsize=7.2, color="#5a6b7b")
            row_xs.append((bx + bw / 2, by + 4.25))
        # 组内箭头
        for i in range(len(row_xs) - 1):
            ax.add_patch(FancyArrowPatch(row_xs[i], row_xs[i + 1],
                                         arrowstyle="-|>", mutation_scale=11,
                                         color=color, lw=1.4))
        xs.append(row_xs)
        ys.append(color)
    # 组间箭头
    for gi in range(ng - 1):
        p1 = (xs[gi][-1][0] + 7.5 / (len(xs[gi])) + 0.4, 21.75)
        p2 = (xs[gi + 1][0][0] - 7.5 / (len(xs[gi + 1])) - 0.4, 21.75)
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                     color="#8a97a5", lw=2.0, linestyle="--"))

    ax.text(50, 3.4, note or "", ha="center", va="center", fontsize=9.5, color="#5a6b7b")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10, color="#1f2d3d")
    fig.savefig(os.path.join(OUT, out), dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


DONE = ""

# 根路线图
draw(
    [
        ("阶段 A · 面试硬基础", [f"{DONE} 01 概率", f"{DONE} 02 推断", f"{DONE} 03 时序"],
         ["12章·48题", "5章·30题", "7章·30题"]),
        ("阶段 B · 核心区分度 ★", [f"{DONE} 04 严谨性"], ["7章·30题"]),
        ("阶段 C · 差异化进阶", [f"{DONE} 05 贝叶斯", f"{DONE} 06 组合"], ["4章·20题", "5章·25题"]),
        ("终点 · 自测", [f"{DONE} 07 题卡"], ["129题"]),
    ],
    "statistics-for-qs · 学习路径总览",
    "path_root.png",
    note="7/7 模块已完成 · 能力库定位：知识 + 题卡 + 方法（不属于 QS 项目集）",
)

# 01 概率
draw(
    [
        ("① 概率基础", [f"{DONE} 01 计数", f"{DONE} 02 贝叶斯", f"{DONE} 03 分布"], ["", "", ""]),
        ("② 期望技巧", [f"{DONE} 04 期望方差", f"{DONE} 05 联合条件"], ["", ""]),
        ("③ 极限与过程", [f"{DONE} 06 LLN/CLT", f"{DONE} 07 游走鞅", f"{DONE} 12 分布关系"], ["", "", ""]),
        ("④ 专题冲刺", [f"{DONE} 08 经典题", f"{DONE} 10 不等式", f"{DONE} 11 几何", f"{DONE} 09 题卡"],
         ["", "", "", "48题"]),
    ],
    "01 概率与组合 · 学习路径",
    "path_01.png",
)

# 02 推断
draw(
    [
        ("① 参数与推断", [f"{DONE} 01 参数估计", f"{DONE} 02 假设检验"], ["MLE/区间", "p值/功效"]),
        ("② 回归与降维", [f"{DONE} 03 回归推断", f"{DONE} 04 降维因子"], ["Fama-MacBeth", "PCA"]),
        ("③ 校正与自测", [f"{DONE} 05 多重检验", f"{DONE} 06 题卡"], ["BH-FDR/t≥3", "30题"]),
    ],
    "02 统计推断 · 学习路径",
    "path_02.png",
)

# 03 时序
draw(
    [
        ("① 序列性质", [f"{DONE} 01 平稳性", f"{DONE} 02 自相关"], ["ADF/KPSS", "Hurst/方差比"]),
        ("② 建模", [f"{DONE} 03 ARMA", f"{DONE} 04 协整", f"{DONE} 05 波动率"], ["", "EG/Johansen", "GARCH"]),
        ("③ 进阶结构", [f"{DONE} 06 状态空间", f"{DONE} 07 随机过程"], ["Kalman/HMM", "GBM/OU"]),
        ("④ 自测", [f"{DONE} 08 题卡"], ["30题"]),
    ],
    "03 时间序列 · 学习路径",
    "path_03.png",
)

# 04 严谨性
draw(
    [
        ("① 证据起点", [f"{DONE} 01 IC 显著性"], ["HAC t"]),
        ("② 防泄漏验证", [f"{DONE} 02 泄漏控制", f"{DONE} 03 CPCV"], ["purge/embargo", "N/K 折"]),
        ("③ 过拟合校正", [f"{DONE} 04 DSR/PSR", f"{DONE} 05 PBO", f"{DONE} 06 多重检验"], ["", "", "BH-FDR"]),
        ("④ 整体与自测", [f"{DONE} 07 整体检验", f"{DONE} 08 题卡"], ["Reality Check", "30题"]),
    ],
    "04 回测严谨性 · 学习路径（核心）",
    "path_04.png",
)

# 05 贝叶斯
draw(
    [
        ("① 推断基础", [f"{DONE} 01 贝叶斯推断"], ["共轭/收缩"]),
        ("② 计算", [f"{DONE} 02 PyMC"], ["MCMC"]),
        ("③ 结构化", [f"{DONE} 03 分层模型", f"{DONE} 04 Regime"], ["", ""]),
        ("④ 自测", [f"{DONE} 05 题卡"], ["20题"]),
    ],
    "05 贝叶斯 · 学习路径",
    "path_05.png",
)

# 06 组合
draw(
    [
        ("① 风险输入", [f"{DONE} 01 协方差估计"], ["收缩"]),
        ("② 风险度量", [f"{DONE} 02 VaR/CVaR", f"{DONE} 03 回撤"], ["", ""]),
        ("③ 仓位与归因", [f"{DONE} 04 Kelly", f"{DONE} 05 归因"], ["", "IC-Sharpe"]),
        ("④ 自测", [f"{DONE} 06 题卡"], ["25题"]),
    ],
    "06 组合与风险 · 学习路径",
    "path_06.png",
)
