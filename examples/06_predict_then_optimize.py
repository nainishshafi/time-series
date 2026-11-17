"""End-to-end Predict-Then-Optimize: Prophet demand forecast -> OR-Tools inventory optimization."""

import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp
from prophet import Prophet


def optimize_replenishment(
    dates: pd.Series,
    demand: list[float],
    min_safety_stock: list[float],
    init_inv: float = 40.0,
    max_cap: float = 200.0,
) -> pd.DataFrame:
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise RuntimeError("SCIP solver not available.")

    T = len(demand)
    holding_cost = 0.50
    unit_cost = 4.00
    fixed_order_cost = 50.0

    I = [solver.NumVar(min_safety_stock[t], max_cap, f"I_{t}") for t in range(T)]
    Q = [solver.NumVar(0, max_cap, f"Q_{t}") for t in range(T)]
    Y = [solver.BoolVar(f"Y_{t}") for t in range(T)]

    solver.Minimize(
        sum(holding_cost * I[t] + unit_cost * Q[t] + fixed_order_cost * Y[t] for t in range(T))
    )

    for t in range(T):
        prev_inv = init_inv if t == 0 else I[t - 1]
        solver.Add(I[t] == prev_inv + Q[t] - demand[t])
        solver.Add(Q[t] <= max_cap * Y[t])

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError("Optimization failed to find an optimal plan.")

    print(f"Total Optimal Cost (14 days): ${solver.Objective().Value():,.2f}")
    return pd.DataFrame({
        "date": dates.dt.strftime("%Y-%m-%d"),
        "forecast_demand": np.round(demand, 1),
        "safety_stock_floor": np.round(min_safety_stock, 1),
        "order_qty": [round(Q[t].solution_value(), 1) for t in range(T)],
        "ending_inv": [round(I[t].solution_value(), 1) for t in range(T)],
    })


def run_pipeline() -> pd.DataFrame:
    np.random.seed(123)
    hist_dates = pd.date_range("2024-01-01", periods=180, freq="D")
    hist_demand = 60 + 12 * np.sin(2 * np.pi * np.arange(180) / 7) + np.random.normal(0, 4, 180)
    df_hist = pd.DataFrame({"ds": hist_dates, "y": hist_demand})

    forecaster = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
    forecaster.fit(df_hist)
    future = forecaster.make_future_dataframe(periods=14)
    forecast = forecaster.predict(future).tail(14).reset_index(drop=True)

    point_demand = forecast["yhat"].clip(lower=0).tolist()
    safety_stock = ((forecast["yhat_upper"] - forecast["yhat"]) * 0.5).clip(lower=0).tolist()

    return optimize_replenishment(forecast["ds"], point_demand, safety_stock)


def main() -> None:
    plan = run_pipeline()
    print("\n=== 14-Day Replenishment Plan ===")
    print(plan.to_string(index=False))


if __name__ == "__main__":
    main()
