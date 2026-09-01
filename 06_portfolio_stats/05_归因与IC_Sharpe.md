# 05 归因与 IC-Sharpe（Fundamental Law）

> 面试权重：★★★☆☆ ｜ 难度：高 ｜ 来源：[S4 Ch20][S7] Grinold & Kahn
> 定位：把"超额收益从哪来"拆开——业绩归因 + 信息比率分解。

## 一、教学

### 1.1 业绩归因

把组合超额收益分解为：

- **资产配置贡献**（大类权重 vs 基准）
- **选股贡献**（资产内选择）
- **交互项**

> Brinson 归因是行业标准；买方组合报告标配。

### 1.2 Fundamental Law of Active Management

$$\mathrm{IR} \approx \mathrm{IC} \times \sqrt{\mathrm{BR}}$$

- IR：信息比率（超额/跟踪误差）
- IC：每次预测的相关系数（技能）
- BR：独立预测次数（广度）

### 1.3 三个推论（面试背）

1. **技能低没关系，广度补**：IC=0.05、BR=400 → IR=1.0
2. **过度交易无益**：BR 来自独立预测，相关预测不算
3. **IC 是瓶颈**：提高 IR 先提高 IC（严谨性模块全部内容）

### 1.4 与回测严谨性闭环

因子 IC（04 模块）→ 组合 IR → Sharpe：IC 显著 + 广度足够 → IR 可信。

## 二、例题精讲

**例 1｜Fundamental Law 手算**

IC=0.05、BR=100 → IR ≈ 0.05×10 = 0.5。

**例 2｜广度陷阱**

1000 个高度相关的预测 ≠ 1000 个独立预测 → 有效 BR 小 → IR 虚高。

**例 3｜归因拆解**

组合超额 3%：配置贡献 1.2%、选股贡献 1.6%、交互 0.2% → 能力主要来自选股。

## 三、面试题

**热身**

1. 信息比率？ → 超额/跟踪误差。
2. Fundamental Law 公式？ → IR ≈ IC×√BR。

**核心**

3. IC、BR、IR 分别是什么？ → 技能、广度、结果。
4. 怎么提高 IR？ → 提高 IC 或有效 BR。
5. 归因拆成哪几块？ → 配置/选股/交互。

**进阶**

6. 相关预测为什么没用？ → 有效 BR 打折。
7. IR 与 Sharpe 关系？ → IR 是主动部分，Sharpe 含基准。

## 四、参考

- [S4] Ch20（IC-Sharpe 相关、Fundamental Law）
- [S7] Grinold & Kahn《Active Portfolio Management》Ch1-2
