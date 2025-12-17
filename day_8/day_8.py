import math
from collections import Counter

file = open("input.txt").readlines()
file = [tuple(coords.strip().split(",")) for coords in file]


def pair_key(p1: tuple[str], p2: tuple[str]) -> tuple[tuple[str]]:
    return tuple(sorted((p1, p2)))

def compute_distance(p1: tuple[str], p2: tuple[str]) -> float:
    p1_x, p1_y, p1_z = int(p1[0]), int(p1[1]), int(p1[2])
    p2_x, p2_y, p2_z = int(p2[0]), int(p2[1]), int(p2[2])

    delta_x = p2_x - p1_x
    delta_y = p2_y - p1_y
    delta_z = p2_z - p1_z

    distance = round(math.sqrt(delta_x**2 + delta_y**2 + delta_z**2), 2)
    return distance



def create_sorted_dict(file: list[tuple[str]]) -> dict:
    pair_distances = dict()
    for p1 in file:
        for p2 in file:
            if p1 == p2:
                continue
            distance = compute_distance(p1, p2)
            key = pair_key(p1, p2)
            if key not in pair_distances:
                pair_distances[key] = distance
    return dict(sorted(pair_distances.items(), key=lambda item: item[1]))

sorted_distances = create_sorted_dict(file)



n = len(file) # number of junction boxes
parent = list(range(n))
size = [1] * n

def find(i):
    if parent[i] != i:
        parent[i] = find(parent[i])
    return parent[i]

def union(i, j) -> bool:
    ri, rj = find(i), find(j)
    if ri == rj:
        return False
    # union by size
    if size[ri] < size[rj]:
        ri, rj = rj, ri
    parent[rj] = ri
    size[ri] += size[rj]
    return True # merged two circuits


idx = {p: i for i, p in enumerate(file)}  # coordinate -> index
components = n
last_merge = None
K = 10 if n == 20 else 1000
for (p1, p2), dist in sorted_distances.items():
    if union(idx[p1], idx[p2]):
        components -= 1
        last_merge = (p1, p2)
        if components == 1:
            break


"""
sizes = Counter(find(i) for i in range(n))
largest_three = sorted(sizes.values(), reverse=True)[:3]
answer = largest_three[0] * largest_three[1] * largest_three[2]
print(answer)
"""

x, y = last_merge[0], last_merge[1]

x_X, y_X = int(x[0]), int(y[0])

print(x_X * y_X)

