
file = open("input.txt").readlines()

id_ranges = [r.strip() for r in file if "-" in r]


# Create tuple pairs of ranges and sort by starting ranges
def mutate_ranges(ranges: list[str]) -> list[tuple[int]]:
    for index, r in enumerate(ranges):
        start_range, end_range = r.split("-")
        ranges[index] = (int(start_range), int(end_range))
    ranges.sort(key=lambda x: x[0])
mutate_ranges(id_ranges)

# Merge overlapping ranges
def merge_ranges(ranges: list[str]) -> list[tuple[int]]:
    current = None
    merged_ranges = []
    for index, r in enumerate(ranges):
        if not current:
            current = r 
        if index == 0:
            continue
        if r[0] <= current[1]:
            current = (current[0], max(current[1], r[1]))
        else:
            merged_ranges.append(current)
            current = r
    merged_ranges.append(current)
    return merged_ranges



def count_available_ids(ranges: list[tuple[int]]) -> int:
    total_available_ids = 0
    merged = merge_ranges(ranges)
    for r in merged:
        total_available_ids += r[1] - r[0] + 1
    return total_available_ids

print("Number of available ids: " ,count_available_ids(id_ranges))
    

