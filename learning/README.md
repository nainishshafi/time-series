# Time-Series Forecasting & Optimization — Learning Path

A structured, hands-on curriculum for mastering time-series forecasting and mathematical optimization, paired with the runnable scripts in [examples/](file:///c:/Users/naini/time-series/examples).

---

## Table of Contents

1. [Module 1: Time-Series Foundations](file:///c:/Users/naini/time-series/learning/01-time-series-foundations.md)
   - Decomposition (Trend, Seasonality, Residuals)
   - Stationarity & Differencing
   - Temporal Train/Test Splits & Leakage Prevention
   - Error Metrics (MAE, RMSE, MAPE, WAPE)
2. [Module 2: Meta Prophet Deep Dive](file:///c:/Users/naini/time-series/learning/02-prophet-deep-dive.md)
   - Additive vs. Multiplicative Models
   - Piecewise Trend & Changepoints
   - Fourier Seasonality & Custom Holidays
   - External Regressors & Rolling Cross-Validation
3. [Module 3: ARIMA, SARIMA & SARIMAX Deep Dive](file:///c:/Users/naini/time-series/learning/03-arima-sarimax-deep-dive.md)
   - Intuition Behind AR($p$), I($d$), MA($q$)
   - Seasonal Orders $(P, D, Q)_m$ & Exogenous $X$
   - Interpreting `results.summary()` & Residual Diagnostics
4. [Module 4: Multivariate LSTMs for Time Series](file:///c:/Users/naini/time-series/learning/04-lstm-sequence-modeling.md)
   - Sliding-Window Framing & 3D Tensor Shapes
   - Inside an LSTM Cell (Forget, Input, Output Gates)
   - PyTorch Training Loop & Avoiding Leakage
   - Common Failure Modes (MSE Lagging & Over-Smoothing)
5. [Module 5: Mathematical Optimization with Google OR-Tools](file:///c:/Users/naini/time-series/learning/05-optimization-modeling-ortools.md)
   - Anatomy of an Optimization Problem
   - LP (Glop) vs. MIP (SCIP) vs. CP-SAT
   - Interval Variables & `add_no_overlap` Scheduling
6. [Module 6: MILP Modeling with Gurobi](file:///c:/Users/naini/time-series/learning/06-milp-with-gurobi.md)
   - Binary Setup Variables & Big-M Linking Constraints
   - Optimality Gap, Status Codes & Licensing Tiers
7. [Module 7: Predict-Then-Optimize Workshop](file:///c:/Users/naini/time-series/learning/07-predict-then-optimize-workshop.md)
   - The Point-Forecast Pitfall
   - Dynamic Safety Stock from Prediction Intervals
   - Multi-Period Inventory Balance & Rolling Horizons

---

## Prerequisites

- Python 3.11+ with `.venv` activated (see [README.md](file:///c:/Users/naini/time-series/README.md))
- Basic familiarity with `numpy`, `pandas`, and linear algebra
