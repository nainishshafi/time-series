# Gurobi Optimizer (`gurobipy`)

**Gurobi** is a commercial mathematical optimization solver widely regarded as the industry benchmark for **MILP** (Mixed-Integer Linear Programming), **MIQCP** (Mixed-Integer Quadratically-Constrained Programming), and **MINLP**. Its Python API (`gurobipy`) offers concise modeling, vectorized matrix APIs (`addMVar`), and callbacks for custom cutting planes or lazy constraints.

---

## Licensing Overview

- **Pip Evaluation License:** `pip install gurobipy` includes a built-in size-limited license (**up to 2,000 variables and 2,000 linear constraints**, or 200 variables for quadratic models)—ideal for learning and prototyping.
- **Academic License:** Free, full-featured, unlimited model size for students, faculty, and university researchers.
- **Commercial Licenses:** Named-user, single-machine, and floating/cloud cluster licenses for production enterprise workloads.

---

## Real-World Use Cases

- **Enterprise Supply Chain & Network Design:** Multi-echelon facility location, sourcing, and transportation planning.
- **Energy & Power Systems:** Unit commitment, economic dispatch, and grid transmission expansion.
- **Finance:** Mean-variance portfolio optimization with cardinality, turnover, and regulatory constraints.
- **Manufacturing & Telecom:** Production line balancing, cutting stock, and 5G/fiber network routing.

---

## Runnable Sample

See [05_gurobi_milp.py](file:///c:/Users/naini/time-series/examples/05_gurobi_milp.py) for a facility/production MILP using binary setup decisions and continuous production variables:

```powershell
.\.venv\Scripts\python.exe examples/05_gurobi_milp.py
```
