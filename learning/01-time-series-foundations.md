# Module 1: Time-Series Foundations

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md)

## Table of Contents

- [1. What Makes Time Series Different?](#1-what-makes-time-series-different)
- [2. Classical Decomposition](#2-classical-decomposition)
- [3. Stationarity & Differencing](#3-stationarity--differencing)
- [4. Temporal Splits & Data Leakage](#4-temporal-splits--data-leakage)
- [5. Choosing the Right Error Metric](#5-choosing-the-right-error-metric)
- [6. Checkpoint Exercises](#6-checkpoint-exercises)

---

## 1. What Makes Time Series Different?

Unlike tabular machine learning where rows are assumed independent and identically distributed (i.i.d.), time-series observations are **ordered and autocorrelated**: today's value depends on yesterday's value, calendar effects, and delayed external shocks.

---

## 2. Classical Decomposition

Most business series can be understood as a combination of three components plus noise:

- **Trend ($T_t$):** Long-term upward or downward direction.
- **Seasonality ($S_t$):** Fixed-period repeating cycles (daily, weekly, yearly).
- **Residual / Noise ($\epsilon_t$):** Irregular fluctuations not explained by trend or seasonality.

Two standard forms:
- **Additive:** $y_t = T_t + S_t + \epsilon_t$ (seasonal amplitude stays constant as trend grows).
- **Multiplicative:** $y_t = T_t \times S_t \times \epsilon_t$ (seasonal swings scale proportionally with the level).

---

## 3. Stationarity & Differencing

A series is **weakly stationary** if its mean, variance, and autocorrelation structure do not change over time. Classical models like ARIMA require stationarity:

- **First differencing ($d=1$):** $y'_t = y_t - y_{t-1}$ removes a linear trend.
- **Seasonal differencing ($D=1$):** $y''_t = y_t - y_{t-m}$ removes a repeating cycle of length $m$ (e.g., $m=12$ for monthly data).

---

## 4. Temporal Splits & Data Leakage

Never use random `train_test_split` on time series—it leaks future patterns into training. Always use:
- **Holdout split:** Train on $[0, t_{\text{split}})$, evaluate on $[t_{\text{split}}, T]$.
- **Rolling / Expanding-Window Cross-Validation:** Repeatedly train up to cutoff $t_k$ and evaluate over horizon $h$ (e.g., Prophet's `cross_validation`).

---

## 5. Choosing the Right Error Metric

| Metric | Formula | When to Use |
| :--- | :--- | :--- |
| **MAE** | $\frac{1}{n}\sum \|y_t - \hat{y}_t\|$ | Easy to interpret in original units; robust to outliers |
| **RMSE** | $\sqrt{\frac{1}{n}\sum (y_t - \hat{y}_t)^2}$ | Penalizes large errors heavily |
| **MAPE** | $\frac{100}{n}\sum \left\|\frac{y_t - \hat{y}_t}{y_t}\right\|$ | Scale-free, but explodes when $y_t \approx 0$ |
| **WAPE** | $\frac{\sum \|y_t - \hat{y}_t\|}{\sum \|y_t\|}$ | Preferred in retail/supply chain across low- and high-volume SKUs |

---

## 6. Checkpoint Exercises

1. Inspect `examples/01_prophet_forecast.py` and `examples/02_sarimax_forecast.py` to see how both enforce chronological splits.
2. Why does MAPE fail on intermittent demand (days with $0$ sales), and why does WAPE solve it?
