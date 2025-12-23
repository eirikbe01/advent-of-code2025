


file = open("input.txt").readlines()
file = [list(line.strip()) for line in file]


def count_timelines(grid: list[list[str]]) -> int:
    start_index = grid[0].index("S")

    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    # ways[column] = number of timelines currently at column 'col' on previous row
    ways = [0] * WIDTH

    ways[start_index] = 1
    #previous_row = grid[1]
    timelines_exited = 0

    for row in grid[2:]:
        next_ways = [0] * WIDTH
        for index, char in enumerate(row):
            count_here = ways[index]
            if count_here == 0:
                continue

            if char == "^":
                left = index - 1
                right = index + 1

                if 0 <= left < WIDTH:
                    next_ways[left] += count_here
                else:
                    timelines_exited += count_here

                if 0 <= right < WIDTH:
                    next_ways[right] += count_here
                else:
                    timelines_exited += count_here
            else:
                # no splitter: keep going straight down
                next_ways[index] += count_here

        ways = next_ways
        #previous_row = row  # kept for your structure, not strictly needed

    # We stopped at the last row already stored in previous_row loop,
    # so any timelines still in `ways` will exit out the bottom.
    timelines_exited += sum(ways)

    return timelines_exited

print(count_timelines(file))


