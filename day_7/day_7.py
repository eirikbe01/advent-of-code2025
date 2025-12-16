


file = open("input.txt").readlines()
file = [list(line.strip()) for line in file]
"""
print("File: ", file)
for line in file:
    print(line, end="")
"""


def has_splitter(char: str):
    if char == "^":
        return True
    else:
        return False

def has_beam(char: str):
    if char == "|":
        return True
    else:
        return False

print()
def draw_beams_and_count(grid: list[str]) -> int:
    previous_row = grid[1]
    start_index = grid[0].index("S")
    grid[1][start_index] = "|"
    num_splits = 0
    for row in grid[2:]:
        for index, char in enumerate(row):
            if char == "^":
                if previous_row[index] == "|":
                    num_splits += 1
                if 1 <= index < len(row)-1:
                    row[index+1] = "|"
                    row[index-1] = "|"
                
            elif previous_row[index] == "|":
                row[index] = "|"
        previous_row = row
    print("\n".join("".join(row) for row in grid))
    return num_splits

print(draw_beams_and_count(file))


