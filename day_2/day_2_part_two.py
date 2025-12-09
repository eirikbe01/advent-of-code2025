
file = open("input.txt", "r")
ranges = file.read().split(",")
id_sum = 0

for r in ranges:
    splitted = r.split("-")
    start_range, end_range = int(splitted[0]), int(splitted[1])


    for id in range(start_range, end_range+1):

        id_str = str(id)
        n = len(id_str)


        invalid = False
        for k in range(1, n // 2 + 1):
            if n % k != 0:
                continue
            block = id_str[:k]

            repeated = block * (n // k)
            # Repeated block and at least two repeats
            if repeated == id_str and (n // k >= 2):
                print("INVALD ID: ", id_str)
                invalid = True
                id_sum += int(id_str)
                break

        if invalid:
            continue

print("SUM OF ALL IDs: ", id_sum)

    


    



