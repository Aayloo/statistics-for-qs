# 04_backtest_rigor ★ · 回测严谨性

核心模块：为什么大多数回测不可信，以及如何用统计检验识别过拟合与数据挖掘。内容来自 [S2][S4][S5]。

| 子主题 | 内容 | 来源 |
| --- | --- | --- |
| 01 信号显著性 | IC/IR、t 统计、IC 衰减 | [S2 Q32][S4 Ch7] |
| 02 泄漏控制 | 前视偏差、purge/embargo、walk-forward | [S2 Q52][S5] |
| 03 CPCV | Combinatorial Purged CV、回测路径重建 | [S5] |
| 04 DSR/PSR | Deflated / Probabilistic Sharpe Ratio | [S4 Ch16][S5] |
| 05 PBO | CSCV 回测过拟合概率 | [S5] |
| 06 因子显著门槛 | Harvey-Liu t≥3、因子动物园、BH-FDR 应用 | [S2 因子工厂][S4 Ch7] |
| 07 整体检验 | White's Reality Check、RAS（Rademacher Anti-Serum） | [S4 Ch16] |

参考：purgedcv 代码 [S5]；deflated-sharpe（mnemox-ai）；AFML [S7]

输出物：每子主题一个 notebook（概念 + 手写实现 + 与开源实现对拍）。
