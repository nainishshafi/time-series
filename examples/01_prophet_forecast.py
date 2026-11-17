"""Prophet forecasting example with custom holidays, external regressors, and cross-validation."""

import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics


def run_prophet_forecast() -> tuple[pd.DataFrame, pd.DataFrame]:
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
    trend = np.linspace(50, 150, len(dates))
    weekly = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    promo = np.random.binomial(1, 0.1, size=len(dates))

    df = pd.DataFrame({
        "ds": dates,
        "y": trend + weekly + promo * 35 + np.random.normal(0, 5, len(dates)),
        "promo": promo,
    })

    custom_holidays = pd.DataFrame({
        "holiday": "big_sale_event",
        "ds": pd.to_datetime(["2023-07-15", "2023-11-25", "2024-07-15", "2024-11-23"]),
        "lower_window": 0,
        "upper_window": 1,
    })

    model = Prophet(
        holidays=custom_holidays,
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.add_country_holidays(country_name="US")
    model.add_regressor("promo")
    model.fit(df)

    future = model.make_future_dataframe(periods=30)
    future["promo"] = 0
    future.loc[future["ds"].isin(["2025-01-05", "2025-01-15"]), "promo"] = 1

    forecast = model.predict(future)
    df_cv = cross_validation(
        model,
        initial="365 days",
        period="90 days",
        horizon="30 days",
    )
    metrics = performance_metrics(df_cv)
    return forecast, metrics


def main() -> None:
    forecast, metrics = run_prophet_forecast()
    print("=== 30-Day Forecast (Tail) ===")
    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper", "promo"]].tail().to_string(index=False))
    print("\n=== Cross-Validation Metrics (Head) ===")
    print(metrics[["horizon", "rmse", "mae", "mape"]].head().to_string(index=False))


if __name__ == "__main__":
    main()
