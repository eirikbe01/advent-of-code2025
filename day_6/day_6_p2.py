from math import prod

file = open("input.txt").readlines()
file = [line.rstrip("\n") for line in file]

# Pad all rows to equal width to index columns safely
W = max(len(line) for line in file)
file = [line.ljust(W) for line in file]

# Split input into operator and digit rows
op_row = file[-1]
digit_rows = file[:-1]
H = len(file)

# Find where the operators are (each one is one problem)
op_cols = [i for i, ch in enumerate(op_row) if ch in "+*"]

# Optional: detect "true separator columns" (blank in every row)
is_sep = [all(file[r][c] == " " for r in range(H)) for c in range(W)]

# Build cut points between adjacent operators so each operator gets its own block
cuts = [-1]
for a, b in zip(op_cols, op_cols[1:]):
    sep_candidates = [c for c in range(a + 1, b) if is_sep[c]]
    if sep_candidates:
        mid = (a + b) // 2
        cut = min(sep_candidates, key=lambda c: abs(c - mid))
    else:
        cut = (a + b) // 2
    cuts.append(cut)
cuts.append(W)

# Now compute each problem
eq_sums = []
for idx, op_c in enumerate(op_cols):
    start = cuts[idx] + 1
    end = cuts[idx + 1]

    op = op_row[op_c]

    # ensure operator column is inside the slice
    if not (start <= op_c < end):
        start = min(start, op_c)
        end = max(end, op_c + 1)

    # COLUMN is a number, read top->bottom, right->left
    numbers = []
    col = end - 1
    while col >= start:
        digits = []
        for row in digit_rows:
            ch = row[col]
            if ch.isdigit():
                digits.append(ch)
        if digits:
            numbers.append(int("".join(digits)))
        col -= 1

    if op == "+":
        eq_sums.append(sum(numbers))
    else:
        eq_sums.append(prod(numbers))

print(sum(eq_sums))
