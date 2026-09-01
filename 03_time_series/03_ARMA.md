# 03 ARMA / ARIMA 模型

> 面试权重：★★★☆☆ ｜ 难度：中→高 ｜ 来源：[S2 Q11][S3 T2]
> 定位：把"记忆"写成模型——预测、去噪、生成模拟数据的标准工具。

## 一、教学

### 1.1 模型族

**AR(p)**（自回归）：依赖自身过去

$$X_t = \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t$$

**MA(q)**（移动平均）：依赖过去冲击

$$X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$$

**ARMA(p,q)** = AR + MA；**ARIMA(p,d,q)** = 先差分 d 次再 ARMA。

### 1.2 定阶

- **ACF 截断** → MA(q)；**PACF 截断** → AR(p)
- **信息准则**：AIC = −2·ℓ + 2k，BIC 惩罚更重（k·ln n）——越小越好

### 1.3 预测

AR(1) 的一步预测：X̂ₜ₊₁ = φ·Xₜ；多步预测向均值回归。

### 1.4 预测回归与稳健标准误

用 Xₜ 预测未来收益 rₜ₊ₖ（重叠样本）→ 残差自相关 → 必须用 HAC 标准误（否则 t 检验虚高）。

### 1.5 VAR（多元）

把多个序列放进向量自回归：互相预测、Granger 因果检验。

## 二、例题精讲

**例 1｜AR(1) 预测**

Xₜ = 0.5Xₜ₋₁ + εₜ，X₅₀ = 2 → X̂₅₁ = 1，X̂₅₂ = 0.5……几何衰减回 0。

**例 2｜AIC 定阶**

AR(1)/AR(2)/AR(3) 的 AIC：−100 / −105 / −103 → 选 AR(2)（AIC 最小）。

**例 3｜重叠预测的坑**

月频特征预测 12 个月收益 → 残差高度重叠相关 → t 统计虚高 → Newey-West 修正后可能不显著。

## 三、面试题

**热身**

1. AR vs MA 区别？ → 依赖自身过去 vs 依赖过去冲击。
2. ARIMA 的 d？ → 差分阶数。

**核心**

3. ACF/PACF 定阶规则？ → ACF 截断 MA、PACF 截断 AR。
4. AIC vs BIC？ → 都是越小越好，BIC 对参数惩罚更重。
5. 重叠样本为什么用 HAC？ → 残差自相关，普通 SE 低估。

**进阶**

6. AR(1) 平稳条件？ → |φ| < 1。
7. VAR 能做什么？ → 多序列互预测、Granger 因果。

## 四、参考

- [S3] Empirical Method Topic 2（ARMA、预测回归、VAR、Kalman）
- [S7] Tsay Ch3-4；statsmodels `ARIMA` / `VAR`
