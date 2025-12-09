



puzzle_input = open("input.txt").readlines()
grid = [list(line.strip()) for line in puzzle_input]


paper_rolls = 0
print(len(grid)-1)
print(len(grid[0])-1)
for row in range(len(grid)):
    for col in range(len(grid[0])):
        if grid[row][col] == "@":
            # Check adjacent cells
            adjacent_positions = [
                (row+1, col), (row, col+1),
                (row-1, col), (row, col-1),
                (row-1, col+1), (row-1, col-1),
                (row+1, col+1), (row+1, col-1)
            ]
            adjacent = 0
            for (adj_row, adj_col) in adjacent_positions:
                if (0 <= adj_row < len(grid) and 0 <= adj_col < len(grid[0])):
                    if grid[adj_row][adj_col] == "@":
                        adjacent += 1

            if adjacent < 4:
                paper_rolls += 1

print("Paper rolls: ", paper_rolls)