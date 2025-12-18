

file = open("input.txt").readlines()
file = [tuple(line.strip().split(","))for line in file]

print(file)

def pair_key(p1: tuple[str], p2: tuple[str]) -> tuple[tuple[str]]:
    return tuple(sorted((p1, p2)))


n = len(file)
area_pairs = dict()
for i in range(n):
    for j in range(i+1, n):
        key = pair_key(file[i], file[j])
        if key in area_pairs:
            continue

        delta_col = abs(int(file[i][0]) - int(file[j][0])) + 1
        delta_row = abs(int(file[i][1]) - int(file[j][1])) + 1
        area = delta_col * delta_row

        area_pairs[key] = area

max_item = max(area_pairs.items(), key=lambda item: item[1])

print(f"The maximum area is {max_item[1]} with tiles {max_item[0]}")
