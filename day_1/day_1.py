

from pathlib import Path


DIAL_SIZE = 100
raw_pointer = 50
password = 0

input_path = Path(__file__).with_name('input.txt')

for line in input_path.read_text().splitlines():
    direction = line[0]
    distance = int(line[1:])
    if direction == 'L':
        distance = -distance

    start = raw_pointer
    raw_pointer += distance

    if distance > 0:
        password += raw_pointer // DIAL_SIZE - start // DIAL_SIZE
    elif distance < 0:
        # Include the end point when moving left so landing on zero counts.
        password += (start - 1) // DIAL_SIZE - (raw_pointer - 1) // DIAL_SIZE

    pointer = raw_pointer % DIAL_SIZE

print(f"Password is: {password}")
