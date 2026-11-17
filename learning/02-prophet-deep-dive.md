# Module 2: Meta Prophet Deep Dive

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [01_prophet_forecast.py](file:///c:/Users/naini/time-series/examples/01_prophet_forecast.py)

## Table of Contents

- [1. Model Equation & Intuition](#1-model-equation--intuition)
- [2. Piecewise Trend & Changepoints](#2-piecewise-trend--changepoints)
- [3. Fourier Seasonality & Custom Holidays](#3-fourier-seasonality--custom-holidays)
- [4. External Regressors](#4-external-regressors)
- [5. Rolling Cross-Validation](#5-rolling-cross-validation)
- [6. Hands-On Exercises](#6-hands-on-exercises)

---

## 1. Model Equation & Intuition

Prophet fits a Generalized Additive Model (GAM):

$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

Because each term is additive, you can inspect `forecast[['trend', 'weekly', 'yearly', 'holidays']]` directly to explain *why* a forecast moved.

---

## 2. Piecewise Trend & Changepoints

- **Linear growth (default):** Piecewise linear segments joined at changepoints.
- **Logistic growth (`growth='logistic'`):** Saturates at a `cap` (and optional `floor`) column—useful for user adoption or market-cap ceilings.
- **Tuning flexibility:** `changepoint_prior_scale` (default `0.05`) controls how aggressively the trend bends. Higher values (`0.1`–`0.5`) fit sharp shifts; lower values (`0.001`) smooth out noise.

---

## 3. Fourier Seasonality & Custom Holidays

- Prophet represents periodic curves using truncated Fourier series.
- **Custom Holidays:** Pass a DataFrame with `holiday`, `ds`, and optional `lower_window` / `upper_window` (e.g., `upper_window=1` in [01_prophet_forecast.py](file:///c:/Users/naini/time-series/examples/01_prophet_forecast.py) captures day-after-sale carryover).
- **Country Holidays:** `model.add_country_holidays(country_name="US")` loads regional calendars automatically.

---

## 4. External Regressors

Use `model.add_regressor("promo")` for known future drivers (promotions, price changes, weather). Every regressor column **must** exist in both the training `df` and the `future` DataFrame passed to `model.predict(future)`.

---

## 5. Rolling Cross-Validation

`cross_validation(model, initial="365 days", period="90 days", horizon="30 days")` trains on expanding windows and evaluates 30-day forecasts at each 90-day cutoff, then `performance_metrics(df_cv)` aggregates RMSE, MAE, and MAPE by horizon.

---

## 6. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/01_prophet_forecast.py` and observe how `promo=1` on `2025-01-05` and `2025-01-15` lifts `yhat`.
2. Change `changepoint_prior_scale` from `0.05` to `0.5` and compare `rmse` in `performance_metrics(df_cv)`.
3. Switch `seasonality_mode="multiplicative"` and test on a series whose weekly swing grows with the trend.
