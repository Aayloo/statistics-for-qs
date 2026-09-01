# 📐 02_inference · 统计推断

QS 的"第二张门票"——不会推断，就看不懂自己的回测结果。

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Chapters](https://img.shields.io/badge/Chapters-5-blueviolet)
![Questions](https://img.shields.io/badge/Questions-30-orange)
![Figures](https://img.shields.io/badge/Figures-5-green)

> JD 证据：hypothesis testing、statistical inference、regression（真实岗位要求，2026-09 检索）
> 公式规范：独立公式用 LaTeX 渲染，正文用 Unicode，无乱码。

## 🎯 定位

从样本数据到结论的数学：MLE 把参数估对，假设检验判"显不显著"，回归推断读出因子溢价，多重检验防止被假阳性骗。每一章按"教学（概念 + 图）→ 例题精讲 → 面试题（热身/核心/进阶）→ 参考"组织。

## 🗺️ 学习路径

```mermaid
flowchart LR
    A[01 参数估计] --> B[02 假设检验]
    B --> C[03 回归推断]
    C --> D[04 降维与因子]
    D --> E[05 多重检验]
    E --> F[06 面试题卡 30 题]
```

## 📚 章节地图

| # | 章节 | 核心主题 | 链接 |
| --- | --- | --- | --- |
| 01 | 参数估计 | MLE、置信区间、对数似然 | [打开](01_参数估计.md) |
| 02 | 假设检验 | p 值、两类错误、功效 | [打开](02_假设检验.md) |
| 03 | 回归推断 | OLS 假设、稳健 SE、Fama-MacBeth | [打开](03_回归推断.md) |
| 04 | 降维与因子 | PCA/SVD、因子模型 | [打开](04_降维与因子.md) |
| 05 | 多重检验 | Bonferroni、BH-FDR、t≥3 | [打开](05_多重检验.md) |
| 06 | 面试题卡 | 30 题分组刷 + 考前清单 | [打开](06_面试题卡.md) |

## 📊 面试权重

| 主题 | 频率 | 难度 | 说明 |
| --- | --- | --- | --- |
| 01 参数估计 | ★★★★☆ | 中 | MLE 是必答套路 |
| 02 假设检验 | ★★★★★ | 中 | p 值/功效是核心 |
| 03 回归推断 | ★★★★★ | 中→高 | Fama-MacBeth 是因子研究标准工具 |
| 04 降维与因子 | ★★★☆☆ | 高 | PCA 必会，因子模型加分 |
| 05 多重检验 ★ | ★★★★☆ | 高 | 面试"杀手题"，衔接 04 模块 |
| 06 题卡 | — | — | 考前刷 |

## 🖼️ 配图（assets/）

MLE 曲线、t vs 正态、功效曲线、p 值分布与假阳性、OLS 四大假设诊断——`make_figures.py` 可重新生成。

## 📜 来源

- [S1] k3vv0/quant_interview_prep（Statistics 目录，README.ipynb 带代码）
- [S2] awesome-quant-interview（Q5 MLE/GMM、Q6 p 值、Q7 协方差、Q8 SVD、Q33 共线性）
- [S3] Empirical Method in Finance（Topic 1/4：稳健 SE、Fama-MacBeth、PCA）
- [S7] 绿皮书、Tsay、石川《因子投资》
