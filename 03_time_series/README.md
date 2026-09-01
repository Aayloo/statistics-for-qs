# 03_time_series · 时间序列统计

金融时间序列的统计检验，量化面试高频。内容来自 [S2][S3][S4]。

| 子主题 | 内容 | 来源 |
| --- | --- | --- |
| 01 平稳性 | ADF/KPSS、单位根、随机游走假说 | [S2 Q10][S3 T1][S4 Ch9] |
| 02 自相关结构 | ACF/PACF、Ljung-Box、Hurst、方差比检验 | [S2][S3 T2] |
| 03 ARMA/ARIMA | 预测回归、自相关稳健标准误、VAR | [S2 Q11][S3 T2] |
| 04 协整 | Engle-Granger、Johansen | [S2 Q12] |
| 05 波动率 | GARCH、已实现波动率、EWMA、VaR 应用 | [S2 Q11][S3 T3] |
| 06 状态空间 | Kalman Filter、HMM regime | [S3 T2][S4 Ch9] |
| 07 随机过程 | GBM、随机游走 | [S2 Q14] |

参考：Tsay《Analysis of Financial Time Series》[S7]；statsmodels / arch 库

输出物：每子主题一个 notebook（检验实现 + 合成数据演示 + 面试题）。
