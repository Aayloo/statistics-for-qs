# 02_inference · 统计推断（从样本到结论）

> 面试权重：★★★★★ ｜ 定位：QS 的"第二张门票"——不会推断，就看不懂自己的回测结果。
> JD 证据：hypothesis testing、statistical inference、regression（真实岗位要求，2026-09 检索）
> 公式规范：独立公式用 $$...$$ 渲染，正文用 Unicode 文本（无内联 LaTeX）。

## 学习路径

```mermaid
flowchart LR
    A[01 参数估计 MLE/区间] --> B[02 假设检验 p值/功效]
    B --> C[03 回归推断 OLS/Fama-MacBeth]
    C --> D[04 降维与因子 PCA/SVD]
    D --> E[05 多重检验 ★ BH-FDR/t≥3]
    E --> F[06 面试题卡 30 题]
```

## 面试权重

| 主题 | 频率 | 难度 | 说明 |
| --- | --- | --- | --- |
| 01 参数估计 | ★★★★☆ | 中 | MLE 是必答套路 |
| 02 假设检验 | ★★★★★ | 中 | p 值/功效是核心 |
| 03 回归推断 | ★★★★★ | 中→高 | Fama-MacBeth 是因子研究标准工具 |
| 04 降维与因子 | ★★★☆☆ | 高 | PCA 必会，因子模型加分 |
| 05 多重检验 ★ | ★★★★☆ | 高 | 与 04 模块衔接，面试"杀手题" |
| 06 题卡 | — | — | 考前刷 |

## 文件

- [01_参数估计.md](01_参数估计.md) —— MLE、置信区间 + 对数似然图
- [02_假设检验.md](02_假设检验.md) —— p 值、两类错误、功效 + t/正态对比图
- [03_回归推断.md](03_回归推断.md) —— OLS 假设、稳健 SE、Fama-MacBeth + 诊断图
- [04_降维与因子.md](04_降维与因子.md) —— PCA/SVD、因子模型
- [05_多重检验.md](05_多重检验.md) —— Bonferroni、BH-FDR、Harvey-Liu t≥3 + p 值分布图
- [06_面试题卡.md](06_面试题卡.md) —— 30 题分组刷

## 配图（assets/）

MLE 曲线、t vs 正态、功效曲线、p 值分布与假阳性、OLS 四大假设诊断——`make_figures.py` 可重新生成。

## 来源

- [S1] k3vv0/quant_interview_prep（Statistics 目录，README.ipynb 带代码）
- [S2] awesome-quant-interview（Q5 MLE/GMM、Q6 p 值、Q7 协方差、Q8 SVD、Q33 共线性）
- [S3] Empirical Method in Finance（Topic 1/4：稳健 SE、Fama-MacBeth、PCA）
- [S7] 绿皮书、Tsay、石川《因子投资》
