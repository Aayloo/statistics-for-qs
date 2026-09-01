# 设计说明 · 公开资源整合 + 缺口分析

> 做法：不自己发明框架，直接摘取公开资源里现成的统计内容，统一格式整合，标注来源；
> 并对比原框架找缺口、给出设计结论。

## 1. 统一框架（01-07）

| 模块 | 内容 | 定位 |
| --- | --- | --- |
| 01_probability | 计数、分布、条件概率与贝叶斯、LLN/CLT、期望/方差/协方差矩阵 | 面试硬基础 |
| 02_inference | MLE/GMM、假设检验、回归推断（Fama-MacBeth/稳健SE）、PCA/SVD、多重检验 | 面试硬基础 |
| 03_time_series | 平稳性、自相关、ARMA、协整、GARCH、Kalman/HMM、GBM | 面试硬基础 |
| 04_backtest_rigor ★ | IC显著性、泄漏控制、CPCV、DSR/PSR、PBO、t≥3门槛、Reality Check | 核心模块 |
| 05_bayesian | 贝叶斯推断、PyMC、分层模型、regime switching | 差异化进阶 |
| 06_portfolio_stats | 协方差估计、VaR/CVaR、回撤、Kelly、归因 | 差异化进阶 |
| 07_practice | 概率/统计/时序题卡 + 考前速查 | 贯穿 |

## 2. 缺口分析

原框架偏"工具清单"、缺"题驱动"。公开资源的统计部分几乎都是「题 + 概念 + 课程」结构，因此：

| # | 原框架漏的 | 公开资源依据 | 处置 |
| --- | --- | --- | --- |
| G1 | 组合数学/计数题 | [S1] 四大块之一；绿皮书/Heard on the Street 高频 | 补进 01_probability |
| G2 | 线性代数基础（EVD/SVD） | [S2 Q8]；[S3 T4] 的 PCA 依赖它 | 并入 02_inference/04 |
| G3 | 回归推断细节：Fama-MacBeth、稳健标准误、多重共线性 | [S3 T1/T4]；[S2 Q33] | 并入 02_inference/03 |
| G4 | 随机过程/GBM | [S2 Q14] | 并入 03_time_series/07 |
| G5 | 因子显著门槛（Harvey-Liu t≥3） | [S2 因子工厂]；[S4 Ch7] | 并入 04/06 |
| G6 | 独立白板题卡模块 | [S1] 四块、[S7] 三本书全是题驱动 | 独立 07_practice |
| G7 | VaR/CVaR 与 GARCH 联动 | [S3 T3]；[S4 Ch19] | 06/02 明确接 03/05 |

**结论**：01-03+07 直接采用公开结构；04-06 把公开资源只给概念的部分做成可展示工具。本模块独立存在，不与其他项目绑定。

## 3. 来源

S1 [quant_interview_prep](https://github.com/k3vv0/quant_interview_prep) ｜ S2 [awesome-quant-interview](https://github.com/SoYuCry/awesome-quant-interview) ｜ S3 [Empirical Method in Finance](https://github.com/Snowrr/Empirical-Method-in-Finance) ｜ S4 [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) ｜ S5 [purgedcv](https://github.com/eslazarev/purged-cross-validation) ｜ S6 [quantitative-finance-notebooks](https://github.com/patrick-t98/quantitative-finance-notebooks) ｜ S7 书目（绿皮书、Heard on the Street、Joshi、Blitzstein & Hwang、Tsay、AFML、石川《因子投资》）
