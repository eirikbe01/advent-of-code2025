puzzle_input = open("input.txt").readlines()
puzzle_input = [bank.strip() for bank in puzzle_input]

total_joltage = 0
for bank in puzzle_input:
    k = max(len(bank) - 12, 0)
    stack = []

    for battery in bank:
        while k > 0 and stack and stack[-1] < battery:
            stack.pop()
            k -= 1
        stack.append(battery)

    # Cut of the rest from the right if still digits to be removed
    # e.g. 435672 with k=2 -> 4356
    if k > 0:
        stack = stack[:-k]
    
    joltage = "".join(stack)
    #print(joltage)
    total_joltage += int(joltage)

        
print("Total voltage: ", total_joltage)