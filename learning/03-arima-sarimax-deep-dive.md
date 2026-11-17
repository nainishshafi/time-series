# Module 3: ARIMA, SARIMA & SARIMAX Deep Dive

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [02_sarimax_forecast.py](file:///c:/Users/naini/time-series/examples/02_sarimax_forecast.py)

## Table of Contents

- [1. Intuition Behind AR, I, and MA](#1-intuition-behind-ar-i-and-ma)
- [2. Seasonal Orders & Exogenous Variables](#2-seasonal-orders--exogenous-variables)
- [3. Code Walkthrough (`statsmodels`)](#3-code-walkthrough-statsmodels)
- [4. Interpreting Diagnostics](#4-interpreting-diagnostics)
- [5. Hands-On Exercises](#5-hands-on-exercises)

---

## 1. Intuition Behind AR, I, and MA

An **ARIMA$(p, d, q)$** model has three building blocks:

- **AR($p$) — AutoRegressive:** Predicts $y_t$ as a linear combination of its own $p$ past values ($y_{t-1}, \dots, y_{t-p}$).
- **I($d$) — Integrated:** Differences the series $d$ times to achieve stationarity.
- **MA($q$) — Moving Average:** Uses $q$ past forecast errors ($\epsilon_{t-1}, \dots, \epsilon_{t-q}$) to correct the current prediction.

---

## 2. Seasonal Orders & Exogenous Variables

- **SARIMA$(p, d, q) \times (P, D, Q)_m$:** Applies the same AR/I/MA structure at seasonal lags of period $m$ (e.g., $m=12$ for monthly data).
- **SARIMAX:** Adds linear regression on exogenous covariates $X_t$ (such as `marketing_spend` in [02_sarimax_forecast.py](file:///c:/Users/naini/time-series/examples/02_sarimax_forecast.py)).

---

## 3. Code Walkthrough (`statsmodels`)

1. Split chronologically: `y_train, y_test = series.iloc[:-12], series.iloc[-12:]`.
2. Instantiate `SARIMAX(endog=y_train, exog=X_train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))`.
3. Fit via maximum likelihood (`model.fit(disp=False)`).
4. Call `results.get_forecast(steps=12, exog=X_test)` to obtain both `predicted_mean` and `conf_int()`.

---

## 4. Interpreting Diagnostics

When printing `results.summary()`:
- **AIC / BIC:** Lower values indicate better trade-off between fit and parameter count.
- **Ljung-Box (`Prob(Q)`):** Tests whether residuals are white noise ($p > 0.05$ is desirable).
- **Coefficient `P>|z|`:** Checks whether each AR/MA/exogenous term is statistically significant.

---

## 5. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/02_sarimax_forecast.py` and inspect how closely `forecast` tracks `actual`.
2. Print `results.summary()` inside `run_sarimax_forecast()` and check the estimated coefficient on `marketing_spend` (true value in the synthetic generator is `1.5`).
3. Remove `exog=X_train` and `exog=X_test` to measure how much accuracy is lost without marketing spend.
