import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def solve_machine_milp(list_of_masks, target):
    """
    Minimize total number of presses:
        minimize sum(x_j)
        subject to A x = target
                 x_j >= 0 and integer
    where each button/mask increments a subset of counters by +1.
    """
    target = tuple(target)
    n = len(target)
    m = len(list_of_masks)

    if n == 0:
        return 0
    if m == 0:
        return 0 if all(t == 0 for t in target) else -1

    # Build A (n x m) where A[i, j] = 1 if mask j increments counter i
    A = np.zeros((n, m), dtype=float)
    for j, mask in enumerate(list_of_masks):
        for idx in mask:
            if 0 <= idx < n:
                A[idx, j] = 1.0

    b = np.array(target, dtype=float)

    # quick infeasible: a counter needs >0 but no button ever increments it
    row_sums = A.sum(axis=1)
    for i in range(n):
        if b[i] > 0 and row_sums[i] == 0:
            return -1

    # objective: minimize total presses
    c = np.ones(m, dtype=float)

    # bounds:
    # x_j cannot exceed min(target[i]) among counters it increments (otherwise overshoot)
    upper_bounds = np.zeros(m, dtype=float)
    for j in range(m):
        rows = np.where(A[:, j] == 1.0)[0]
        if len(rows) == 0:
            upper_bounds[j] = 0.0
        else:
            upper_bounds[j] = float(min(b[i] for i in rows))

    bounds = Bounds(np.zeros(m), upper_bounds)

    # A x == b
    constraints = LinearConstraint(A, b, b)

    # all integer variables
    integrality = np.ones(m, dtype=int)

    result = milp(c=c, integrality=integrality, constraints=constraints, bounds=bounds)

    if not result.success:
        return -1

    return int(round(result.fun))


file = open("input.txt").readlines()
file = [line.split(" ") for line in file]

total_presses = 0
for machine in file:
    machine_presses = 0

    # pre-processing
    indicator, wire_schema, jolt_req = machine[0], machine[1:-1], machine[-1]
    jolt_req = [int(x.strip()) for x in jolt_req.strip().strip("{}").split(",")]

    wire_schema = [
        tuple(int(x.strip()) for x in points.strip("()").split(",") if x.strip())
        for points in wire_schema
    ]

    # Solve for minimal number of presses
    machine_presses += solve_machine_milp(wire_schema, jolt_req)

    total_presses += machine_presses

print(f"Total number of minimal presses: {total_presses}")
