
puzzle_input = open("input.txt").readlines()
grid = [list(line.strip()) for line in puzzle_input]

def clean_grid(grid: list[list[int]]):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "x":
                grid[row][col] = "."

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def remove_paper_rolls(grid: list[list[int]], positions: list[tuple[int, int]], removed=False):
    for row, col in positions:
        if removed:
            grid[row][col] = "x"
        else:
            grid[row][col] = "x"


total_rolls = 0
while True:
    paper_rolls = 0
    positions_to_remove = []
    clean_grid(grid)
    print("State: ")
    print_grid(grid)
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
                    positions_to_remove.append((row, col))
                    total_rolls += 1
    
    if paper_rolls == 0:
        break
    
    remove_paper_rolls(grid, positions_to_remove)
    print(f"Removing {paper_rolls} rolls of paper: ")
    print_grid(grid)

print("Total rolls: ", total_rolls)