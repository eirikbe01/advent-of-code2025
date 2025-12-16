file = open("input.txt").readlines()

# Clean data
operations = [entry for entry in list(file[-1]) if entry != " "]
equations = [equation.strip().split() for equation in list(file[:-1])]

# Transpose equations matrix
eq_transformed = []
index = 0
while index < len(equations[0]):
    new = []
    for equation in equations:
        new.append(int(equation[index]))
    index += 1
    eq_transformed.append(new)

# Calculate sums of the different equations
eq_sums = []
for index, equation in enumerate(eq_transformed):
    if operations[index] == "+":
        eq_sums.append(sum(equation))
    else:
        eq_sum = 1
        for number in equation:
            eq_sum *= number
        eq_sums.append(eq_sum)

# Total sum of the equations
print(sum(eq_sums))


