"""Google OR-Tools examples: CP-SAT job-shop scheduling and pywraplp (SCIP) MIP."""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model


def solve_job_shop() -> float:
    model = cp_model.CpModel()

    jobs_data = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0: (machine_id, duration)
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3)],          # Job 2
    ]
    num_machines = 3
    horizon = sum(duration for job in jobs_data for _, duration in job)

    all_tasks = {}
    machine_to_intervals = {m: [] for m in range(num_machines)}

    for job_id, job in enumerate(jobs_data):
        prev_end = None
        for task_id, (machine, duration) in enumerate(job):
            suffix = f"_{job_id}_{task_id}"
            start = model.new_int_var(0, horizon, f"start{suffix}")
            end = model.new_int_var(0, horizon, f"end{suffix}")
            interval = model.new_interval_var(start, duration, end, f"interval{suffix}")

            all_tasks[job_id, task_id] = (start, end, machine)
            machine_to_intervals[machine].append(interval)

            if prev_end is not None:
                model.add(start >= prev_end)
            prev_end = end

    for m in range(num_machines):
        model.add_no_overlap(machine_to_intervals[m])

    makespan = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        makespan, [all_tasks[j, len(job) - 1][1] for j, job in enumerate(jobs_data)]
    )
    model.minimize(makespan)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    print("=== CP-SAT Job-Shop Scheduling ===")
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"Optimal Makespan: {solver.objective_value}")
        for (j, t), (start, end, machine) in sorted(all_tasks.items()):
            print(f"  Job {j} Task {t} (Machine {machine}): [{solver.value(start)}, {solver.value(end)}]")
        return float(solver.objective_value)
    raise RuntimeError("No feasible schedule found.")


def solve_mip() -> tuple[float, float, float]:
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise RuntimeError("SCIP solver not available.")

    x = solver.IntVar(0, 10, "x")
    y = solver.NumVar(0, solver.infinity(), "y")

    solver.Add(x + 2 * y <= 14.0)
    solver.Add(3 * x - y <= 0.0)
    solver.Maximize(3 * x + 4 * y)

    print("\n=== pywraplp (SCIP) MIP ===")
    if solver.Solve() == pywraplp.Solver.OPTIMAL:
        obj = float(solver.Objective().Value())
        x_val = float(x.solution_value())
        y_val = float(y.solution_value())
        print(f"Optimal Objective: {obj:.2f}")
        print(f"x = {x_val}, y = {y_val:.2f}")
        return obj, x_val, y_val
    raise RuntimeError("No optimal solution found.")


if __name__ == "__main__":
    solve_job_shop()
    solve_mip()
