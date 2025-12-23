from collections import deque

lines = open("input.txt").read().strip().splitlines()
reds = [tuple(map(int, line.split(","))) for line in lines]
n = len(reds)

# ------------------------------------------------------------
# 1) Coordinate compression (use reds plus +/-1 padding)
# ------------------------------------------------------------
xs = set()
ys = set()
for x, y in reds:
    xs.update((x - 1, x, x + 1))
    ys.update((y - 1, y, y + 1))

xs = sorted(xs)
ys = sorted(ys)
x_to_i = {x: i for i, x in enumerate(xs)}
y_to_j = {y: j for j, y in enumerate(ys)}

W = len(xs)
H = len(ys)

# These weights tell how many original tile-columns/rows each compressed *cell* represents.
# Cell (r,c) corresponds to x in [xs[c], xs[c+1]] and y in [ys[r], ys[r+1]] in tile coordinates.
dx = [xs[i + 1] - xs[i] for i in range(W - 1)]
dy = [ys[j + 1] - ys[j] for j in range(H - 1)]

# We'll work on CELL grid (H-1) x (W-1)
CW = W - 1
CH = H - 1

def idx(r, c):
    return r * CW + c

# ------------------------------------------------------------
# 2) Mark boundary walls on the compressed *cell* grid
# ------------------------------------------------------------
# We'll store "blocked edges" between neighboring cells.
# Vertical walls: block moving left<->right across a boundary at some x index.
# Horizontal walls: block moving up<->down across a boundary at some y index.
#
# Use two bitsets:
#   block_lr[r][c] blocks movement between cell (r,c-1) and (r,c)  (a wall on vertical line xs[c])
#   block_ud[r][c] blocks movement between cell (r-1,c) and (r,c)  (a wall on horizontal line ys[r])
#
# Dimensions:
#   block_lr: CH x (CW+1)  (vertical grid lines)
#   block_ud: (CH+1) x CW  (horizontal grid lines)

block_lr = [bytearray(CW + 1) for _ in range(CH)]
block_ud = [bytearray(CW) for _ in range(CH + 1)]

def add_vertical_wall(x, y1, y2):
    # wall lies on vertical grid line at x, spanning y in [miny, maxy]
    i = x_to_i[x]  # vertical line index
    a, b = sorted((y1, y2))
    ja = y_to_j[a]
    jb = y_to_j[b]
    # spans cell-rows between ja..jb-1 in cell space
    for r in range(min(ja, jb), max(ja, jb)):
        if 0 <= r < CH and 0 <= i <= CW:
            block_lr[r][i] = 1

def add_horizontal_wall(y, x1, x2):
    j = y_to_j[y]  # horizontal line index
    a, b = sorted((x1, x2))
    ia = x_to_i[a]
    ib = x_to_i[b]
    for c in range(min(ia, ib), max(ia, ib)):
        if 0 <= c < CW and 0 <= j <= CH:
            block_ud[j][c] = 1

# The path is along rows/cols between consecutive red points (wrap)
for k in range(n):
    x1, y1 = reds[k]
    x2, y2 = reds[(k + 1) % n]
    if x1 == x2:
        add_vertical_wall(x1, y1, y2)
    elif y1 == y2:
        add_horizontal_wall(y1, x1, x2)
    else:
        raise ValueError("Consecutive points must share x or y")

# ------------------------------------------------------------
# 3) Flood fill OUTSIDE on the compressed cell grid, using walls
# ------------------------------------------------------------
outside = bytearray(CH * CW)
q = deque()

def push(r, c):
    if 0 <= r < CH and 0 <= c < CW:
        p = idx(r, c)
        if not outside[p]:
            outside[p] = 1
            q.append((r, c))

# Start from border cells as "outside"
for c in range(CW):
    push(0, c)
    push(CH - 1, c)
for r in range(CH):
    push(r, 0)
    push(r, CW - 1)

while q:
    r, c = q.popleft()

    # left
    if c > 0 and not block_lr[r][c]:
        push(r, c - 1)
    # right
    if c + 1 < CW and not block_lr[r][c + 1]:
        push(r, c + 1)
    # up
    if r > 0 and not block_ud[r][c]:
        push(r - 1, c)
    # down
    if r + 1 < CH and not block_ud[r + 1][c]:
        push(r + 1, c)

# inside = not outside
# allowed region = inside OR boundary-path cells; but since the boundary is a 1-tile-thick loop,
# treating the wall as the boundary is enough for "rectangle must stay inside".
# We'll require rectangle to be inside (not outside). (Corners are guaranteed red anyway.)

# ------------------------------------------------------------
# 4) Build WEIGHTED prefix sum for "inside" area (in original tile counts)
# ------------------------------------------------------------
# inside_weight[r][c] = dx[c] * dy[r] if inside else 0
ps = [[0] * (CW + 1) for _ in range(CH + 1)]

for r in range(CH):
    run = 0
    for c in range(CW):
        p = idx(r, c)
        w = (dx[c] * dy[r]) if (outside[p] == 0) else 0
        run += w
        ps[r + 1][c + 1] = ps[r][c + 1] + run

def inside_area(r1, c1, r2, c2):
    return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1]

# ------------------------------------------------------------
# 5) Rectangle check (must be fully inside)
# Rectangle between red tiles (x1,y1) and (x2,y2) includes ALL tiles in inclusive range.
# Convert that to cell-range in compressed coordinates:
# x tiles [minx..maxx] -> x-span [minx..maxx+1] in edge coords -> columns between indices.
# Since xs list contains minx and maxx+1? Not necessarily, so we included +/-1, but not +1 for all.
# We handle it by using minx and maxx+1 explicitly; if missing, reject.
# ------------------------------------------------------------
def rect_ok(x1, y1, x2, y2):
    minx, maxx = (x1, x2) if x1 <= x2 else (x2, x1)
    miny, maxy = (y1, y2) if y1 <= y2 else (y2, y1)

    # inclusive tiles => edge span [minx, maxx+1], [miny, maxy+1]
    xL, xR = minx, maxx + 1
    yT, yB = miny, maxy + 1

    if xL not in x_to_i or xR not in x_to_i or yT not in y_to_j or yB not in y_to_j:
        return False

    c1 = x_to_i[xL]
    c2 = x_to_i[xR] - 1
    r1 = y_to_j[yT]
    r2 = y_to_j[yB] - 1

    if c1 > c2 or r1 > r2:
        return False

    rect_area = (maxx - minx + 1) * (maxy - miny + 1)
    # In compressed cells, area is sum(dx*dy) over the span.
    return inside_area(r1, c1, r2, c2) == rect_area

# ------------------------------------------------------------
# 6) Enumerate red pairs (O(n^2) ~ 125k for n=500)
# ------------------------------------------------------------
best_area = 0
best_pair = None

for i in range(n):
    x1, y1 = reds[i]
    for j in range(i + 1, n):
        x2, y2 = reds[j]
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if area <= best_area:
            continue
        if rect_ok(x1, y1, x2, y2):
            best_area = area
            best_pair = ((x1, y1), (x2, y2))

print("best_area:", best_area)
print("best_pair:", best_pair)