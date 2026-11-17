# ARIMA / SARIMA / SARIMAX (`statsmodels`)

The **ARIMA** family is the foundation of classical statistical time-series forecasting:

- **ARIMA$(p, d, q)$:** Combines AutoRegressive ($p$ lags), Integrated ($d$ differencing orders for stationarity), and Moving Average ($q$ lagged forecast errors) terms.
- **SARIMA$(p, d, q) \times (P, D, Q)_m$:** Adds seasonal AR, differencing, and MA terms with period $m$ (e.g., $m=12$ for monthly data, $m=7$ for daily data with weekly cycles).
- **SARIMAX:** Extends SARIMA with **exogenous regressors ($X$)** such as weather, pricing, or promotional flags.

In Python, `statsmodels.tsa.statespace.sarimax.SARIMAX` implements all three variants in a unified state-space framework.

> [!TIP]
> For automated order selection $(p, d, q)(P, D, Q)_m$ via AIC/BIC, use `pmdarima.auto_arima`. For high-throughput forecasting across thousands of series, consider Nixtla's `statsforecast` (Numba-accelerated `AutoARIMA`).

---

## Real-World Use Cases

- **Macroeconomics:** Forecasting GDP growth, inflation, interest rates, and unemployment.
- **Energy & Utilities:** Short-term hourly/daily electricity and natural gas load forecasting using temperature as an exogenous variable.
- **Retail & Inventory:** Store- or SKU-level short-horizon demand forecasting with calendar and promo covariates.
- **Finance:** Short-term rate/spread modeling (often paired with GARCH for volatility).

---

## Limitations

- **Linearity & Stationarity:** Assumes linear relationships and requires differencing to stabilize mean/variance.
- **Long-Horizon Degradation:** Multi-step forecasts converge toward a mean or linear trend with rapidly widening confidence intervals.
- **Structural Breaks:** Sudden regime shifts (e.g., supply shocks) invalidate historical parameters until re-estimated.
- **Manual Order Selection:** Traditional ACF/PACF inspection can be subjective without automated AIC/BIC search.

---

## Runnable Sample

See [02_sarimax_forecast.py](file:///c:/Users/naini/time-series/examples/02_sarimax_forecast.py) for a complete `SARIMAX` script with exogenous regressors and 95% confidence intervals:

```powershell
.\.venv\Scripts\python.exe examples/02_sarimax_forecast.py
```
