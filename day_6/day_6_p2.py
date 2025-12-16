import numpy as np

file = open("example_input.txt").readlines()
print("Raw file: ", file)
file = [line.strip("\n") for line in file]
print("Processed raw: ", file)
grid_width = len(file[0])

for line in file:
    if len(line) < grid_width:
        while len(line) < grid_width:
            line += " "

print(file)

rows = len(file)
last_row = rows-1
grid = file[:-1]
print(grid)
# Clean data
operations = [entry for entry in list(file[-1]) if entry != " "]
print(operations)
equations = [equation.rstrip("\n").split(" ") for equation in list(file[:-1])]


for col in range(grid_width):
    if col == "":
        pass
print(equations)
equations.reverse()
print(equations)


# Transpose equations matrix
eq_transformed = []
index = 0
while index < len(equations[0]):
    new = []
    for equation in equations:
        new.append(equation[index])
    index += 1
    eq_transformed.append(new)

print("V1: ", eq_transformed)
"""
eq_transformed_v2 = []
for eq in eq_transformed:
    num_columns = len(max(eq, key=len))
    new_eq = []
    for num in eq:
        if len(num) < num_columns:
            while len(num) < num_columns:
                num = "-" + num
        new_eq.append(list(num))
    eq_transformed_v2.append(new_eq)
print("V2: ",eq_transformed_v2)

eq_transformed_v3 = []
for eq in eq_transformed_v2:
    new_eq = []
    index = 0
    while index < len(eq):
        new_nums = []
        for number in eq:
            new_nums.append(number[index])
        index += 1
        #print(new_nums)
        new_eq.append("".join(new_nums))
    eq_transformed_v3.append(new_eq)
print("V3: ", eq_transformed_v3)
    
"""



"""
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
"""
