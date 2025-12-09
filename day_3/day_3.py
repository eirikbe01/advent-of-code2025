puzzle_input = open("input.txt").readlines()
puzzle_input = [bank.strip() for bank in puzzle_input]

total_voltage = 0
for bank in puzzle_input:
    joltages = []
    for i in range(len(bank)):
        for j in range(len(bank)):
            if i == j:
                continue
            if i > j:
                continue
            joltages.append(str(bank[i]) + str(bank[j]))
    print(max(joltages))
    total_voltage += int(max(joltages))

print("Total Voltage: ", total_voltage)

