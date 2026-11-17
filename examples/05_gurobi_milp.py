"""Gurobi (gurobipy) MILP example: facility setup and production planning."""

import gurobipy as gp
from gurobipy import GRB


def solve_production_milp() -> tuple[float, float, float]:
    with gp.Env() as env, gp.Model("production_plan", env=env) as m:
        open_plant = m.addVar(vtype=GRB.BINARY, name="open_plant")
        units = m.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=500.0, name="units")

        m.setObjective(8 * units - 1000 * open_plant, GRB.MAXIMIZE)
        m.addConstr(units <= 500 * open_plant, name="capacity_link")
        m.addConstr(units >= 100 * open_plant, name="min_batch")

        m.optimize()

        if m.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Optimization ended with status {m.Status}")

        return float(m.ObjVal), float(open_plant.X), float(units.X)


def main() -> None:
    obj_val, open_val, units_val = solve_production_milp()
    print("\n=== Gurobi MILP Result ===")
    print(f"Optimal Profit: ${obj_val:,.2f}")
    print(f"open_plant = {open_val}, units = {units_val}")


if __name__ == "__main__":
    main()
