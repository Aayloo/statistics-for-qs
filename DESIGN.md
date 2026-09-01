# 设计说明 · QS 统计模块（岗位需求证据 + 最优框架）

> 做法：不自己发明框架，先检索真实 QS 岗位 JD 提炼统计需求，再对照公开资源（题仓库、课程、书）给出最优目录。
> 版本：2026-09-01 ｜ 原则：**能力库定位**——与 ML/DL/LLM 学习库平行；不属于 QS 项目集（alpha signal / portfolio 构建），不产出策略项目。

## 0. 定位（与项目集的区别）

- **QS 项目集**：alpha 信号研究、组合构建、多资产配置等——产出策略与研报。
- **本仓库（能力库）**：统计知识与面试方法论——产出教学笔记、题卡、严谨性方法，与 ML/DL/LLM 能力库同级、平行。
- **关系**：项目集提供"做了什么"，能力库提供"凭什么可信"。本仓库不替代项目，也不属于项目集。

## 1. QS 岗位要什么统计（JD 证据，2026-09 检索）

| 真实 JD 要求（摘录） | 对应统计能力 |
| --- | --- |
| "Strong foundations in statistics and econometrics: time-series analysis, regression, cointegration, factor modelling, and hypothesis testing" | 时间序列计量 + 回归推断 |
| "Statistical inference, regression, stochastic processes, time-series modelling, model validation, and experimental design" | 推断 + 随机过程 + 实验设计 |
| "Probability, statistics, time-series analysis, stochastic processes, optimisation, regression, ML, risk-aware model evaluation" | 全栈概率统计 |
| "Understanding of overfitting risk" | 回测严谨性 |
| "Hypothesis testing, multiple-comparisons correction (Benjamini-Hochberg), walk-forward and purged cross-validation, look-ahead bias prevention, regime-dependent performance" | 多重检验 + 泄漏控制 + 分 regime |
| "IC analysis with HAC-adjusted standard errors; Deflated Sharpe Ratio; Combinatorial Purged CV" | 因子显著性 + DSR + CPCV |

**结论**：QS 的统计需求分三层——①面试白板（概率/推断）②金融计量（时间序列/回归/协整）③研究严谨性（多重检验/DSR/PBO/防泄漏）。前两层是入场券，第三层是买方的核心区分度。

## 2. 最优框架目录（7 模块）

```
statistics-for-qs/
├── README.md                    模块总览 + 学习路径
├── DESIGN.md                    本文件
├── 01_probability ✅ 已完成       概率与组合（12 章 + 48 题 + 10 图）
├── 02_inference ✅ 已完成         统计推断（MLE/假设检验/回归/PCA/多重检验，5 章 + 30 题 + 5 图）
│   ├── 01_参数估计               MLE/GMM、置信区间
│   ├── 02_假设检验               t/z、p 值、功效、I/II 类错误
│   ├── 03_回归推断               OLS 假设、多重共线性、HAC/稳健 SE、Fama-MacBeth
│   ├── 04_降维与因子              PCA/SVD、因子模型
│   └── 05_多重检验               Bonferroni、BH-FDR、Harvey-Liu t≥3
├── 03_time_series ✅ 已完成       时间序列计量（7 章 + 30 题 + 5 图）
│   ├── 01_平稳性                 ADF/KPSS、单位根、随机游走
│   ├── 02_自相关                 ACF/PACF、Ljung-Box、Hurst、方差比
│   ├── 03_ARMA/回归              预测回归、VAR、稳健 SE
│   ├── 04_协整                   Engle-Granger、Johansen
│   ├── 05_波动率                 GARCH、已实现波动率、EWMA
│   ├── 06_状态空间               Kalman、HMM regime
│   └── 07_随机过程               GBM、泊松过程、几何布朗运动
├── 04_backtest_rigor ★ ✅ 已完成  回测严谨性（7 章 + 30 题 + 6 图）
│   ├── 01_IC显著性               IC/IR、HAC t 统计、IC 衰减
│   ├── 02_泄漏控制               look-ahead、purge/embargo、walk-forward
│   ├── 03_CPCV                   Combinatorial Purged CV
│   ├── 04_DSR/PSR                Deflated / Probabilistic Sharpe
│   ├── 05_PBO                    CSCV 过拟合概率
│   ├── 06_多重检验应用           BH-FDR、t≥3、因子动物园
│   └── 07_整体检验              White's Reality Check、RAS
├── 05_bayesian ✅ 已完成          贝叶斯（4 章 + 20 题 + 4 图）
│   ├── 01_推断                  先验/后验、共轭
│   ├── 02_PyMC                  MCMC 实操
│   ├── 03_分层模型                hierarchical 因子
│   └── 04_Regime                贝叶斯状态切换
├── 06_portfolio_stats ✅ 已完成   组合与风险统计（5 章 + 25 题 + 4 图）
│   ├── 01_协方差估计             样本/收缩/EWMA/因子模型
│   ├── 02_VaR/CVaR               尾部风险（接 GARCH）
│   ├── 03_回撤                   回撤分布
│   ├── 04_Kelly                  Kelly 仓位
│   └── 05_归因                   业绩归因、IC-Sharpe
└── 07_practice ✅ 已完成          汇总题卡（129 题含答案 + 10 综合模拟）
    ├── 概率题 / 统计题 / 时序题 / 考前速查
```

## 3. 为什么是这个结构（对照证据）

| 模块 | JD 关键词命中 | 公开资源依据 |
| --- | --- | --- |
| 01 概率 | probability、stochastic processes | [S1][S2][S7] |
| 02 推断 | hypothesis testing、regression、statistical inference | [S1][S2][S3 T1/T4][S6] |
| 03 时序 | time-series analysis、cointegration、econometrics | [S2][S3][S4 Ch9] |
| 04 严谨性 ★ | overfitting、multiple-comparisons、purged CV、DSR | [S4 Ch7/16][S5] |
| 05 贝叶斯 | 差异化（无 JD 硬要求，但 regime/不确定性管理加分） | [S6][S4 Ch15] |
| 06 组合统计 | optimisation、risk-aware evaluation、VaR | [S3 T3][S4 Ch17/19] |
| 07 题卡 | 面试整体 | [S1][S7] |

## 4. 学习顺序与优先级

| 优先级 | 模块 | 理由 |
| --- | --- | --- |
| P0 | 02 推断、03 时序、04 严谨性 | JD 直接点名，且 04 是买方 QS 的区分度 |
| P1 | 06 组合统计、07 题卡 | 组合是 QS 第二大职责；题卡考前刷 |
| P2 | 05 贝叶斯 | 差异化，锦上添花 |

## 5. 缺口分析（原框架 → 最优框架）

原框架偏"工具清单"、缺"题驱动 + 岗位需求锚定"。公开资源的统计部分几乎都是「题 + 概念 + 课程」结构，因此：

| # | 缺口 | 依据 | 处置 |
| --- | --- | --- | --- |
| G1 | 组合数学/计数题 | [S1] 四大块之一；绿皮书高频 | 已并入 01 |
| G2 | 线性代数基础（EVD/SVD） | [S2 Q8]；PCA 依赖 | 并入 02/04 |
| G3 | Fama-MacBeth、稳健 SE、多重共线性 | [S3 T1/T4]；[S2 Q33] | 并入 02/03 |
| G4 | 随机过程/GBM | [S2 Q14] | 并入 03/07 |
| G5 | Harvey-Liu t≥3、因子动物园 | [S2 因子工厂]；[S4 Ch7] | 并入 04/06 |
| G6 | 独立题卡模块 | [S1][S7] 全是题驱动 | 独立 07 |
| G7 | VaR 与 GARCH 联动 | [S3 T3]；[S4 Ch19] | 06/02 接 03/05 |
| G8 | JD 需求锚定（本次新增） | 真实岗位检索 | 本文件第 1、3 节 |

## 6. 来源

S1 [quant_interview_prep](https://github.com/k3vv0/quant_interview_prep) ｜ S2 [awesome-quant-interview](https://github.com/SoYuCry/awesome-quant-interview) ｜ S3 [Empirical Method in Finance](https://github.com/Snowrr/Empirical-Method-in-Finance) ｜ S4 [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) ｜ S5 [purgedcv](https://github.com/eslazarev/purged-cross-validation) ｜ S6 [quantitative-finance-notebooks](https://github.com/patrick-t98/quantitative-finance-notebooks) ｜ S7 书目（绿皮书、Heard on the Street、Joshi、Blitzstein & Hwang、Tsay、AFML、石川《因子投资》）｜ S8 真实 QS/QR JD（2026-09 公开检索）
