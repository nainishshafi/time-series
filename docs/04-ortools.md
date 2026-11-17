# Google OR-Tools

**Google OR-Tools** is an open-source (Apache 2.0) C++ optimization suite with Python, Java, C#, and C++ APIs. It bundles specialized solvers for distinct problem classes:

1. **CP-SAT (Constraint Programming + SAT):** Google's flagship solver for combinatorial scheduling, sequencing, and pure integer programming. Supports native interval variables and global constraints (`AddNoOverlap`, `AddCumulative`, `AddAllDifferent`).
2. **Glop & PDLP:** High-performance Linear Programming (LP) solvers—Glop (simplex) and PDLP (first-order primal-dual hybrid gradient for ultra-large LPs).
3. **MPSolver (`pywraplp`):** Unified wrapper for LP/MIP backends including **SCIP**, **CBC**, **GLOP**, and commercial solvers like **Gurobi**.
4. **Routing Library:** Dedicated engine for **TSP** and **VRP** variants (time windows, vehicle capacities, pickup-and-delivery, heterogeneous fleets).

---

## Solver Selection Inside OR-Tools

| Problem Characteristic | Recommended Solver |
| :--- | :--- |
| Continuous variables, linear constraints, massive scale | **Glop / PDLP** |
| Mixed continuous + integer variables with linear constraints | **MPSolver (`SCIP` / `CBC`)** |
| Scheduling, resource bottlenecks, logical rules, sequencing | **CP-SAT** |
| Moving vehicles, visiting nodes, time windows, distance matrices | **Routing Library** |

---

## Real-World Use Cases

- **Workforce & Shift Scheduling:** Nurse/retail rostering with labor rules, skill matching, and rest constraints (CP-SAT).
- **Manufacturing Job-Shop Scheduling:** Sequencing tasks across machines to minimize makespan or tardiness (CP-SAT).
- **Last-Mile Delivery & Field Service:** Multi-vehicle routing with strict customer time windows and capacities (Routing Library).
- **Cutting Stock & Bin Packing:** Minimizing material waste in 1D/2D cutting or container loading (CP-SAT / MIP).

---

## Runnable Sample

See [04_ortools_scheduling_mip.py](file:///c:/Users/naini/time-series/examples/04_ortools_scheduling_mip.py) for both a **CP-SAT job-shop scheduling** solver and a **`pywraplp` (SCIP) MIP** solver:

```powershell
.\.venv\Scripts\python.exe examples/04_ortools_scheduling_mip.py
```
