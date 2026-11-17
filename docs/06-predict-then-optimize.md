# End-to-End Predict-Then-Optimize Pipeline

In practice, forecasting and mathematical optimization are coupled into a **rolling-horizon pipeline**:

```mermaid
flowchart LR
    A["Historical Sales & Calendar"] --> B["1. Demand Forecaster (Prophet / SARIMAX)"]
    B -->|"Point Forecast + Uncertainty Interval"| C["2. Dynamic Safety Stock"]
    C --> D["3. Inventory Optimizer (OR-Tools / Gurobi)"]
    D -->|"Order Quantities & Timing"| E["4. Replenishment Plan"]
```

1. **Forecast** future demand $\hat{d}_t$ and uncertainty $\hat{\sigma}_t$ (e.g., via Prophet or SARIMAX).
2. **Buffer** against forecast error using dynamic safety stock derived from prediction intervals (or multi-scenario stochastic optimization).
3. **Optimize** replenishment quantities $Q_t$, binary order triggers $Y_t$, and inventory levels $I_t$ to minimize total holding, variable purchase, and fixed setup costs.

---

## Mathematical Formulation

- **Decision Variables:**
  - $I_t \ge \text{SafetyStock}_t$: Ending inventory in period $t$
  - $Q_t \ge 0$: Order quantity in period $t$
  - $Y_t \in \{0, 1\}$: Binary indicator for placing an order in period $t$
- **Objective:**
  $$\min \sum_{t} \left( h \cdot I_t + c \cdot Q_t + K \cdot Y_t \right)$$
- **Constraints:**
  - Inventory balance: $I_t = I_{t-1} + Q_t - \hat{d}_t$
  - Setup linking: $Q_t \le \text{MaxCap} \cdot Y_t$

---

## Production Best Practices

1. **Never optimize on raw point forecasts alone:** Deterministic point forecasts ignore variance and systematically cause stockouts. Inject dynamic safety stock from prediction intervals (`yhat_upper - yhat`) or optimize expected cost across $N$ bootstrapped demand scenarios.
2. **Run on a rolling horizon:** Re-forecast and re-optimize daily/weekly as actual inventory and sales materialize.
3. **Measure end-to-end KPIs:** Track forecast accuracy (RMSE, WAPE) *alongside* business outcomes (total cost, service level / fill rate, waste).

---

## Runnable Sample

See [06_predict_then_optimize.py](file:///c:/Users/naini/time-series/examples/06_predict_then_optimize.py) for a complete pipeline coupling a 14-day **Prophet** demand forecast into an **OR-Tools (SCIP)** multi-period inventory optimization model:

```powershell
.\.venv\Scripts\python.exe examples/06_predict_then_optimize.py
```
