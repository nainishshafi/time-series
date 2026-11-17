# Meta Prophet

**Prophet** is an open-source forecasting library built around an interpretable, decomposable Generalized Additive Model (GAM):

$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$

- **$g(t)$ Trend:** Piecewise linear or logistic growth curves (with a `cap` for saturation limits) and automatic or manual changepoint detection.
- **$s(t)$ Seasonality:** Fourier series modeling daily, weekly, yearly, or custom seasonal cycles.
- **$h(t)$ Holidays & Events:** Irregular schedules with configurable `lower_window` and `upper_window` carryover effects.
- **External Regressors:** Additional known future covariates (e.g., promotions, pricing, weather).

> [!NOTE]
> Prophet is in **maintenance mode** (v1.4.0+), focusing on bug fixes and dependency updates rather than major new features. For neural extensions that retain Prophet's decomposable structure, consider **NeuralProphet** (PyTorch-based).

---

## Real-World Use Cases

- **Retail & E-commerce:** Daily/weekly SKU and category demand forecasting across holiday peaks (Black Friday, Lunar New Year).
- **Infrastructure Capacity Planning:** Predicting server load, API traffic, and cloud compute demand.
- **Finance & Budgeting:** Forecasting revenue, cash flow, and transaction volumes aligned to fiscal calendars.
- **Marketing Analytics:** Separating baseline organic growth from promotional campaign lift.

---

## Best Practices

- **Provide at least 2 full years of history** when modeling yearly seasonality.
- **Leave missing dates as gaps / `NaN`** rather than imputing zeros (unless zero is a true observation).
- **Tune `changepoint_prior_scale`** (default `0.05`): increase (e.g., `0.1`–`0.5`) if underfitting trend shifts; decrease (e.g., `0.001`) if overfitting noise.
- **Disable unused seasonalities** (e.g., `daily_seasonality=False` for daily/monthly data).
- **Supply future regressor values:** Every regressor added via `add_regressor()` must have known values across the entire forecast horizon.
- **Validate temporally:** Use `prophet.diagnostics.cross_validation` and `performance_metrics` instead of random train/test splits.

---

## Runnable Sample

See [01_prophet_forecast.py](file:///c:/Users/naini/time-series/examples/01_prophet_forecast.py) for a complete script demonstrating custom holidays, external regressors, and rolling-window cross-validation:

```powershell
.\.venv\Scripts\python.exe examples/01_prophet_forecast.py
```
