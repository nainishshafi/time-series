# Module 6: MILP Modeling with Gurobi

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [05_gurobi_milp.py](file:///c:/Users/naini/time-series/examples/05_gurobi_milp.py)

## Table of Contents

- [1. Why Gurobi for Enterprise MILP?](#1-why-gurobi-for-enterprise-milp)
- [2. Binary Setup & Big-M Linking Constraints](#2-binary-setup--big-m-linking-constraints)
- [3. Status Codes & Optimality Gap](#3-status-codes--optimality-gap)
- [4. Licensing Tiers](#4-licensing-tiers)
- [5. Hands-On Exercises](#5-hands-on-exercises)

---

## 1. Why Gurobi for Enterprise MILP?

Gurobi combines aggressive **presolve** reductions, cutting planes, primal heuristics, and parallel branch-and-bound—making it the standard choice when large MILP/MIQCP models must solve within tight production SLAs.

---

## 2. Binary Setup & Big-M Linking Constraints

In [05_gurobi_milp.py](file:///c:/Users/naini/time-series/examples/05_gurobi_milp.py):
- `open_plant` is `GRB.BINARY` ($\in \{0, 1\}$), incurring a fixed cost of \$1,000 if opened.
- `units` is `GRB.CONTINUOUS` ($\in [0, 500]$), earning \$8/unit margin.
- **Big-M linking constraint:** `units <= 500 * open_plant` forces `units = 0` whenever `open_plant = 0`, and allows up to `500` units when `open_plant = 1`.
- **Minimum batch constraint:** `units >= 100 * open_plant` enforces a minimum viable run size if the plant is opened.

---

## 3. Status Codes & Optimality Gap

Always check `m.Status` before reading `.X` or `.ObjVal`:
- `GRB.OPTIMAL`: Proven global optimum found.
- `GRB.TIME_LIMIT`: Stopped at `TimeLimit`; check `m.MIPGap` (relative gap between best incumbent and best dual bound) and `m.SolCount > 0`.
- `GRB.INFEASIBLE`: No solution satisfies all constraints; use `m.computeIIS()` to diagnose conflicting constraints.

---

## 4. Licensing Tiers

- **Pip Evaluation:** Bundled with `pip install gurobipy` (limit: **2,000 variables and 2,000 linear constraints**).
- **Academic:** Free, unlimited model size for university students, faculty, and staff.
- **Commercial:** Production licenses for named users, single machines, or cloud clusters.

---

## 5. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/05_gurobi_milp.py` and verify the optimal profit (`$3,000.00`).
2. Increase the fixed setup cost from `1000` to `4500` and see `open_plant` flip to `0.0` (do not open).
3. Add a piecewise or quadratic penalty (e.g., `-0.01 * units * units`) to explore Gurobi's MIQP solver.
