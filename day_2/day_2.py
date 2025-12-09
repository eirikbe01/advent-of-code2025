


file = open("input.txt", "r")
ranges = file.read().split(",")
id_sum = 0

for r in ranges:
    splitted = r.split("-")
    start_range, end_range = int(splitted[0]), int(splitted[1])


    for id in range(start_range, end_range+1):

        id = str(id)
        id_len = len(id)

        #uneven id, can't have a sequence repeated
        if id_len % 2 != 0:
            continue

        # Split in the middle and compare
        middle_index = id_len // 2
        id_start, id_end = id[:middle_index], id[middle_index:id_len]

        if id_start == id_end:
            print("INVALID ID: ", id)
            id_sum += int(id)

print("SUM OF ALL IDs: ", id_sum)

    


    



