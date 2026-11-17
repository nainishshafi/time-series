# Module 7: Predict-Then-Optimize Workshop

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [06_predict_then_optimize.py](file:///c:/Users/naini/time-series/examples/06_predict_then_optimize.py)

## Table of Contents

- [1. The Point-Forecast Pitfall](#1-the-point-forecast-pitfall)
- [2. Turning Prediction Intervals into Safety Stock](#2-turning-prediction-intervals-into-safety-stock)
- [3. Inventory Balance & Fixed-Cost MILP](#3-inventory-balance--fixed-cost-milp)
- [4. Rolling-Horizon Execution](#4-rolling-horizon-execution)
- [5. Hands-On Exercises](#5-hands-on-exercises)

---

## 1. The Point-Forecast Pitfall

If you feed only a point forecast $\hat{d}_t$ into a cost-minimizing inventory optimizer, the solver assumes zero uncertainty and drives ending inventory to $0$ every period. Any positive demand surprise immediately causes a **stockout**.

---

## 2. Turning Prediction Intervals into Safety Stock

In [06_predict_then_optimize.py](file:///c:/Users/naini/time-series/examples/06_predict_then_optimize.py), Prophet outputs both `yhat` and `yhat_upper`. We compute a dynamic daily safety-stock floor:

$$\text{SafetyStock}_t = 0.5 \times (\hat{y}_{\text{upper}, t} - \hat{y}_t)$$

and set `I[t] = solver.NumVar(min_safety_stock[t], max_cap, ...)` so the optimizer must hold enough buffer to absorb forecast uncertainty.

---

## 3. Inventory Balance & Fixed-Cost MILP

For each day $t \in \{0, \dots, 13\}$:
- **Flow conservation:** $I_t = I_{t-1} + Q_t - \hat{d}_t$
- **Setup linking:** $Q_t \le \text{MaxCap} \cdot Y_t$, where $Y_t \in \{0, 1\}$ triggers a \$50 fixed order cost.
- **Trade-off:** Because ordering incurs a \$50 fixed setup cost while holding costs \$0.50/unit/day, the optimizer batches orders across multiple days rather than ordering every single day.

---

## 4. Rolling-Horizon Execution

In production:
1. Run the 14-day forecast + optimization every morning using actual current on-hand inventory `init_inv`.
2. Execute only **today's** order decision $Q_0$.
3. Tomorrow, observe actual sales, update `init_inv`, re-forecast, and re-optimize.

---

## 5. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/06_predict_then_optimize.py` and inspect which days trigger `order_qty > 0`.
2. Lower `fixed_order_cost` from `50.0` to `2.0` and observe how order frequency increases while average `ending_inv` drops.
3. Add a lead time $L = 2$ days (`Q[t - 2]` arriving on day `t`) to the inventory balance constraint.
