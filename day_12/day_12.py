import re

IDX_PAT = re.compile(r"^(\d+):\s*$")
REG_PAT = re.compile(r"^(\d+)x(\d+):\s*(.*)$")

def parse(lines):
    lines = [ln.rstrip("\n") for ln in lines]
    i = 0
    shapes = {}

    # Shapes
    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue

        if REG_PAT.match(ln):
            break

        m = IDX_PAT.match(ln)
        if not m:
            raise ValueError(f"Expected shape index like '0:' but got: {lines[i]}")
        idx = int(m.group(1))
        i += 1

        grid = []
        while i < len(lines):
            ln2 = lines[i].rstrip()
            if not ln2:
                i += 1
                break
            if IDX_PAT.match(ln2.strip()) or REG_PAT.match(ln2.strip()):
                break
            grid.append(ln2)
            i += 1

        area = sum(ch == "#" for row in grid for ch in row)
        shapes[idx] = area

    # normalize shapes into list by index
    max_idx = max(shapes) if shapes else -1
    shape_areas = [shapes[k] for k in range(max_idx + 1)]

    # Tree regions section 
    regions = []
    while i < len(lines):
        ln = lines[i].strip()
        i += 1
        if not ln:
            continue
        m = REG_PAT.match(ln)
        if not m:
            raise ValueError(f"Expected region like '12x5: ...' but got: {ln}")
        W, H = int(m.group(1)), int(m.group(2))
        counts = list(map(int, m.group(3).split())) if m.group(3).strip() else []
        regions.append((W, H, counts))

    return shape_areas, regions

def solve(lines):
    shape_areas, regions = parse(lines)
    ok = 0

    for W, H, counts in regions:
        if len(counts) < len(shape_areas):
            counts = counts + [0] * (len(shape_areas) - len(counts))
        elif len(counts) > len(shape_areas):
            raise ValueError("Region has more counts than there are shapes.")

        required = sum(counts[i] * shape_areas[i] for i in range(len(shape_areas)))
        if required <= W * H:
            ok += 1

    return ok

if __name__ == "__main__":
    file = open("input.txt", "r", encoding="utf-8").readlines()
    print(solve(file))
