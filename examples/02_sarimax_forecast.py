"""SARIMAX forecasting example with exogenous marketing spend and 95% confidence intervals."""

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def run_sarimax_forecast() -> pd.DataFrame:
    np.random.seed(7)
    n_periods = 60
    dates = pd.date_range("2020-01-01", periods=n_periods, freq="MS")
    marketing_spend = np.random.uniform(10, 30, size=n_periods)
    seasonal = 15 * np.sin(2 * np.pi * np.arange(n_periods) / 12)
    y = (
        100
        + 0.8 * np.arange(n_periods)
        + 1.5 * marketing_spend
        + seasonal
        + np.random.normal(0, 3, n_periods)
    )

    series = pd.Series(y, index=dates, name="sales")
    exog = pd.DataFrame({"marketing_spend": marketing_spend}, index=dates)

    y_train, y_test = series.iloc[:-12], series.iloc[-12:]
    X_train, X_test = exog.iloc[:-12], exog.iloc[-12:]

    model = SARIMAX(
        endog=y_train,
        exog=X_train,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    results = model.fit(disp=False)

    forecast_obj = results.get_forecast(steps=12, exog=X_test)
    conf_int = forecast_obj.conf_int()

    return pd.DataFrame({
        "actual": y_test,
        "forecast": forecast_obj.predicted_mean,
        "lower_95": conf_int.iloc[:, 0],
        "upper_95": conf_int.iloc[:, 1],
    })


def main() -> None:
    output = run_sarimax_forecast()
    print("=== 12-Month SARIMAX Forecast vs Actual ===")
    print(output.round(2).to_string())


if __name__ == "__main__":
    main()
