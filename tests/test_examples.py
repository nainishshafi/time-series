"""Pytest suite covering all forecasting, optimization, and predict-then-optimize examples."""

import importlib.util
from pathlib import Path
from types import ModuleType

import numpy as np
import torch

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def _load_example(filename: str) -> ModuleType:
    """Dynamically load an example module by filename."""
    path = EXAMPLES_DIR / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prophet_forecast_and_cv() -> None:
    mod = _load_example("01_prophet_forecast.py")
    forecast, metrics = mod.run_prophet_forecast()

    assert len(forecast) == 731 + 30
    assert {"ds", "yhat", "yhat_lower", "yhat_upper"}.issubset(forecast.columns)
    assert (forecast["yhat_lower"] <= forecast["yhat"]).all()
    assert (forecast["yhat"] <= forecast["yhat_upper"]).all()
    assert not metrics.empty
    assert (metrics["rmse"] > 0).all()


def test_sarimax_forecast_intervals() -> None:
    mod = _load_example("02_sarimax_forecast.py")
    output = mod.run_sarimax_forecast()

    assert len(output) == 12
    assert {"actual", "forecast", "lower_95", "upper_95"}.issubset(output.columns)
    assert (output["lower_95"] <= output["forecast"]).all()
    assert (output["forecast"] <= output["upper_95"]).all()
    mae = np.mean(np.abs(output["actual"] - output["forecast"]))
    assert mae < 15.0


def test_lstm_multivariate_training() -> None:
    mod = _load_example("03_lstm_multivariate.py")
    arr = np.zeros((30, 3), dtype=np.float32)
    X, y = mod.create_windows(arr, seq_len=10)
    assert X.shape == (20, 10, 3)
    assert y.shape == (20, 1)

    model = mod.MultivariateLSTM(input_dim=3, hidden_dim=16, num_layers=1)
    out = model(torch.zeros((4, 10, 3)))
    assert out.shape == (4, 1)

    train_mse, test_mse = mod.run_lstm_experiment(epochs=10)
    assert np.isfinite(train_mse)
    assert test_mse < 0.25


def test_ortools_scheduling_and_mip() -> None:
    mod = _load_example("04_ortools_scheduling_mip.py")
    makespan = mod.solve_job_shop()
    assert makespan == 11.0

    obj, x_val, y_val = mod.solve_mip()
    assert np.isclose(obj, 30.0, atol=1e-6)
    assert np.isclose(x_val, 2.0, atol=1e-6)
    assert np.isclose(y_val, 6.0, atol=1e-6)


def test_gurobi_production_milp() -> None:
    mod = _load_example("05_gurobi_milp.py")
    obj_val, open_val, units_val = mod.solve_production_milp()
    assert np.isclose(obj_val, 3000.0, atol=1e-6)
    assert np.isclose(open_val, 1.0, atol=1e-6)
    assert np.isclose(units_val, 500.0, atol=1e-6)


def test_predict_then_optimize_pipeline() -> None:
    mod = _load_example("06_predict_then_optimize.py")
    plan = mod.run_pipeline()

    assert len(plan) == 14
    assert {"date", "forecast_demand", "safety_stock_floor", "order_qty", "ending_inv"}.issubset(
        plan.columns
    )
    assert (plan["order_qty"] >= 0).all()
    assert (plan["ending_inv"] >= plan["safety_stock_floor"] - 1e-6).all()
