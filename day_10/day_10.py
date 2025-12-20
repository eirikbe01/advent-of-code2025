from collections import deque

def indices_to_mask(indices):
    mask = 0
    for i in indices:
        mask |= 1 << i
    return mask

def vector_to_mask(vec):
    mask = 0
    for i, bit in enumerate(vec):
        if bit:
            mask |= 1 << i
    return mask

def bfs(list_of_masks, target):
    visited = set()
    queue = deque()

    initial_state = (0, 0) # (XOR sum, num_masks)
    queue.append(initial_state)
    visited.add(0)

    while queue:
        curr_xor_sum, count = queue.popleft()

        if curr_xor_sum == target:
            return count
        
        for mask in list_of_masks:
            # Bitwise operation
            next_xor_sum = curr_xor_sum ^ mask
            if next_xor_sum not in visited:
                visited.add(next_xor_sum)
                queue.append((next_xor_sum, count + 1))
    return -1


file = open("input.txt").readlines()
file = [line.split(" ") for line in file]


total_presses = 0
for machine in file:
    machine_presses = 0

    #pre-processing
    indicator, wire_schema, jolt_req = machine[0], machine[1:-1], machine[-1]
    indicator = list(indicator)[1:-1]
    wire_schema = [
        tuple(int(x.strip()) for x in points.strip("()").split(",") if x.strip())
        for points in wire_schema
    ]
    binary_indicator = tuple([0 if char == "." else 1 for char in indicator])

    # Turn diagram into bitwise masks
    target_mask = vector_to_mask(binary_indicator)
    mask_list = [indices_to_mask(t) for t in wire_schema]

    print(f"Indicator: {indicator}, Wire Schema: {wire_schema}, Joltage Req: {jolt_req}")

    # BFS search for minimal number of presses
    machine_presses += bfs(mask_list, target_mask)

    # Update global press variable
    total_presses += machine_presses

print(f"Total number of minimal presses: {total_presses}")
