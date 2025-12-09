
file = open("input.txt").readlines()

id_ranges = [r.strip() for r in file if "-" in r]
available_ids = [int(id) for id in file if "-" not in id and id != "\n"]


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



def count_fresh(ranges: list[tuple[int]], ids: list[int]) -> int:
    num_fresh = 0
    merged = merge_ranges(ranges)
    for id in ids:
        for r in merged:
            if r[0] <= id <= r[1]:
                num_fresh += 1
    return num_fresh

print("Number of fresh ingredients: ", count_fresh(id_ranges, available_ids))
