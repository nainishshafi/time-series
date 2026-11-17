# Time-Series Forecasting & Mathematical Optimization

A modular guide and runnable Python codebase covering **Prophet**, **ARIMA/SARIMAX**, **LSTMs**, **Google OR-Tools**, and **Gurobi**, plus an end-to-end **Predict-then-Optimize** pipeline.

---

## Setup & Running with `.venv`

### 1. Activate the Virtual Environment

On Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

### 2. Install Dependencies (if setting up fresh)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Run Any Example

```powershell
.\.venv\Scripts\python.exe examples/01_prophet_forecast.py
.\.venv\Scripts\python.exe examples/02_sarimax_forecast.py
.\.venv\Scripts\python.exe examples/03_lstm_multivariate.py
.\.venv\Scripts\python.exe examples/04_ortools_scheduling_mip.py
.\.venv\Scripts\python.exe examples/05_gurobi_milp.py
.\.venv\Scripts\python.exe examples/06_predict_then_optimize.py
```

### 4. Run the Test Suite

```powershell
.\.venv\Scripts\pytest.exe -v
```

---

## Documentation Index

### Tool Reference (`docs/`)

| Topic | Guide | Runnable Sample |
| :--- | :--- | :--- |
| **Meta Prophet** | [01-prophet.md](file:///c:/Users/naini/time-series/docs/01-prophet.md) | [01_prophet_forecast.py](file:///c:/Users/naini/time-series/examples/01_prophet_forecast.py) |
| **ARIMA / SARIMA / SARIMAX** | [02-arima-sarimax.md](file:///c:/Users/naini/time-series/docs/02-arima-sarimax.md) | [02_sarimax_forecast.py](file:///c:/Users/naini/time-series/examples/02_sarimax_forecast.py) |
| **LSTMs (PyTorch & Keras)** | [03-lstm.md](file:///c:/Users/naini/time-series/docs/03-lstm.md) | [03_lstm_multivariate.py](file:///c:/Users/naini/time-series/examples/03_lstm_multivariate.py) |
| **Google OR-Tools** | [04-ortools.md](file:///c:/Users/naini/time-series/docs/04-ortools.md) | [04_ortools_scheduling_mip.py](file:///c:/Users/naini/time-series/examples/04_ortools_scheduling_mip.py) |
| **Gurobi Optimizer** | [05-gurobi.md](file:///c:/Users/naini/time-series/docs/05-gurobi.md) | [05_gurobi_milp.py](file:///c:/Users/naini/time-series/examples/05_gurobi_milp.py) |
| **Predict-Then-Optimize Pipeline** | [06-predict-then-optimize.md](file:///c:/Users/naini/time-series/docs/06-predict-then-optimize.md) | [06_predict_then_optimize.py](file:///c:/Users/naini/time-series/examples/06_predict_then_optimize.py) |

### Learning Curriculum (`learning/`)

Start with the [Learning Path Table of Contents](file:///c:/Users/naini/time-series/learning/README.md) for step-by-step modules with internal TOCs and hands-on exercises:

1. [Module 1: Time-Series Foundations](file:///c:/Users/naini/time-series/learning/01-time-series-foundations.md)
2. [Module 2: Meta Prophet Deep Dive](file:///c:/Users/naini/time-series/learning/02-prophet-deep-dive.md)
3. [Module 3: ARIMA, SARIMA & SARIMAX Deep Dive](file:///c:/Users/naini/time-series/learning/03-arima-sarimax-deep-dive.md)
4. [Module 4: Multivariate LSTMs for Time Series](file:///c:/Users/naini/time-series/learning/04-lstm-sequence-modeling.md)
5. [Module 5: Mathematical Optimization with Google OR-Tools](file:///c:/Users/naini/time-series/learning/05-optimization-modeling-ortools.md)
6. [Module 6: MILP Modeling with Gurobi](file:///c:/Users/naini/time-series/learning/06-milp-with-gurobi.md)
7. [Module 7: Predict-Then-Optimize Workshop](file:///c:/Users/naini/time-series/learning/07-predict-then-optimize-workshop.md)

---

## Quick Comparison Matrix

### Forecasting Tools

| Tool | Paradigm | Strengths | Limitations | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Prophet** | Decomposable additive/multiplicative GAM | Fast prototyping; handles missing data, changepoints, holidays, and multiple seasonalities natively | Maintenance mode (v1.4.0+); struggles with complex non-linear interactions or high-frequency autocorrelation | Business metrics (daily/weekly retail sales, web traffic, capacity planning) |
| **ARIMA / SARIMAX** | Classical statistical state-space | Mathematically rigorous; interpretable coefficients; well-calibrated confidence intervals; strong on short horizons | Assumes linearity and stationarity; univariate by default (SARIMAX adds exogenous $X$); flatlines on long horizons | Macroeconomics, short-term demand, energy load, single-series benchmarks |
| **LSTMs** | Deep learning (gated RNN) | Captures non-linear dynamics and multivariate cross-feature interactions natively | Slow sequential training; prone to lag/over-smoothing under MSE; data-hungry; black-box | Multivariate sensor/IoT data, high-frequency energy/traffic, complex multi-feature series |

### Optimization Tools

| Tool | Paradigm | Strengths | Licensing | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Google OR-Tools** | Open-source suite (Glop, PDLP, CP-SAT, Routing, MPSolver) | Best-in-class CP-SAT for scheduling; dedicated VRP/TSP routing engine; free & permissive | Apache 2.0 (Free, open-source) | Workforce/job-shop scheduling, vehicle routing, medium-scale LP/MIP |
| **Gurobi** | Commercial mathematical optimization (MILP, MIQCP, MINLP) | Industry-leading solver speed, presolve, and numerical stability at massive scale | Commercial (Free Academic; Pip eval limited to 2,000 vars / 2,000 linear constraints) | Large-scale enterprise supply chains, energy unit commitment, portfolio optimization |

---

## Decision Guide: Which Tool Should You Choose?

- **Need a fast, interpretable business forecast with holidays & missing data?** → Start with **Prophet**.
- **Need a rigorous short-term statistical benchmark or well-calibrated intervals on a single series?** → Use **SARIMAX** (`statsmodels` or `statsforecast`).
- **Have rich multivariate sequential signals (sensors, weather, traffic) and non-linear dynamics?** → Use **LSTMs** (or modern deep-learning time-series models like Temporal Fusion Transformers / PatchTST).
- **Need workforce scheduling, job-shop sequencing, or vehicle routing with zero licensing cost?** → Use **Google OR-Tools** (`CP-SAT` for scheduling, `Routing` for VRP/TSP, `Glop`/`SCIP` for LP/MIP).
- **Have massive enterprise MILP/MIQCP models where solver runtime directly impacts SLAs?** → Use **Gurobi** (`gurobipy`).
