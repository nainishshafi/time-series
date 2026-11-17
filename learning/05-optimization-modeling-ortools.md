# Module 5: Mathematical Optimization with Google OR-Tools

> Back to [Learning Path TOC](file:///c:/Users/naini/time-series/learning/README.md) · Runnable Script: [04_ortools_scheduling_mip.py](file:///c:/Users/naini/time-series/examples/04_ortools_scheduling_mip.py)

## Table of Contents

- [1. Anatomy of an Optimization Problem](#1-anatomy-of-an-optimization-problem)
- [2. Choosing the Right OR-Tools Solver](#2-choosing-the-right-or-tools-solver)
- [3. CP-SAT Job-Shop Scheduling Walkthrough](#3-cp-sat-job-shop-scheduling-walkthrough)
- [4. `pywraplp` Mixed-Integer Programming Walkthrough](#4-pywraplp-mixed-integer-programming-walkthrough)
- [5. Hands-On Exercises](#5-hands-on-exercises)

---

## 1. Anatomy of an Optimization Problem

Every mathematical optimization model has three parts:
1. **Decision Variables:** Unknown quantities the solver chooses (continuous, integer, binary, or interval).
2. **Constraints:** Rules that feasible solutions must satisfy (capacity, precedence, no-overlap, budgets).
3. **Objective Function:** A scalar expression to **minimize** (cost, makespan, distance) or **maximize** (profit, throughput).

---

## 2. Choosing the Right OR-Tools Solver

| Solver | Best For | Key Primitives |
| :--- | :--- | :--- |
| **CP-SAT** (`cp_model`) | Scheduling, sequencing, logical rules, pure integer problems | `new_int_var`, `new_interval_var`, `add_no_overlap`, `add_max_equality` |
| **Glop / PDLP** (`pywraplp`) | Pure continuous Linear Programming (LP) | `NumVar`, `Add`, `Maximize` / `Minimize` |
| **SCIP / CBC** (`pywraplp`) | Mixed-Integer Linear Programming (MILP) | `IntVar`, `BoolVar`, `NumVar` |
| **Routing** (`pywrapcp`) | Vehicle Routing (VRP) & Traveling Salesman (TSP) | Time windows, capacities, pickup/delivery |

---

## 3. CP-SAT Job-Shop Scheduling Walkthrough

In `solve_job_shop()` inside [04_ortools_scheduling_mip.py](file:///c:/Users/naini/time-series/examples/04_ortools_scheduling_mip.py):
- Each task is modeled with `start`, `end`, and a fixed-duration `interval = model.new_interval_var(start, duration, end, ...)`.
- **Within-job precedence:** `model.add(start >= prev_end)` forces tasks in the same job to run in order.
- **Machine exclusivity:** `model.add_no_overlap(machine_to_intervals[m])` guarantees a machine processes at most one task at a time.
- **Makespan objective:** `model.add_max_equality(makespan, ...)` captures the latest job completion time, and `model.minimize(makespan)` finds the shortest schedule (`11.0`).

---

## 4. `pywraplp` Mixed-Integer Programming Walkthrough

In `solve_mip()`:
- `x` is an integer variable (`IntVar(0, 10, "x")`) and `y` is continuous (`NumVar(0, infinity, "y")`).
- Subject to $x + 2y \le 14$ and $3x - y \le 0$, maximizing $3x + 4y$ yields `x = 2, y = 6.0` with objective `30.0`.

---

## 5. Hands-On Exercises

1. Run `.\.venv\Scripts\python.exe examples/04_ortools_scheduling_mip.py` and verify the Gantt intervals for each machine.
2. Add a 4th job `[(2, 2), (0, 3)]` to `jobs_data` and observe how the optimal makespan changes.
3. In `solve_mip()`, change `x` from `IntVar` to `NumVar` (pure LP) and check whether the optimal objective increases.
