with open("input.txt") as file:
    file_string = [line.rstrip() for line in file]
    range_string = file_string[0]


def hack_way(start, end):
    invalid_sum = 0
    start_len = len(start)
    end_len = len(end)

    if start_len % 2 == 1:
        start_value = '1' + '0' * int(start_len/2)
    else:
        start_value = start[:int(start_len/2)]

    if end_len % 2 == 1:
        end_value = '9' * int(start_len/2)
    else:
        end_value = end[:int(end_len/2)]

    start_int = int(start_value)
    end_int = int(end_value)
    if start_int > end_int:
        return 0

    if int(start_value * 2) < int(start):
        start_int += 1
    if int(end_value * 2) > int(end):
        end_int -= 1

    for i in range(start_int, end_int + 1):
        invalid_sum += int(str(i)*2)
    return invalid_sum

def extensible(start, end, repeat, used_set):
    invalid_sum = 0
    start_len = len(start)
    end_len = len(end)

    if repeat > end_len:
        return 0

    if start_len % repeat == 0:
        start_value = start[:int(start_len/repeat)]
    else:
        start_value = '1' + '0' * int(start_len/repeat)

    if end_len % repeat == 0:
        end_value = end[:int(end_len/repeat)]
    else:
        end_value = '9' * int(end_len/repeat)

    start_int = int(start_value)
    end_int = int(end_value)

    if int(start_value * repeat) < int(start):
        start_int += 1
    if int(end_value * repeat) > int(end):
        end_int -= 1

    if start_int > end_int:
        return 0

#    print(start, end, start_value, end_value, int(str(start_int) * repeat), int(str(end_int) * repeat))

    for i in range(start_int, end_int + 1):
        value = int(str(i)*repeat)
        if value not in used_set:
            invalid_sum += value
            used_set.add(value)
    return invalid_sum

range_split = range_string.split(",")
total = 0
for range_string in range_split:
    ranges = range_string.split('-')
    start = ranges[0]
    end = ranges[1]
    used_set = set()
#    total += extensible(start, end, 10)
#    print(start, end, 'total', total)
    for i in range(2, len(end)+1):
        total += extensible(start, end, i, used_set)
print(total)
#2case: 43952536386
# case: 54486209192
# mine: 54811879987
# diff: 325,670,795

# to find sequences repeated twice
# 17 - 47
# 22, 33, 44

# 1751 - 4283
# 1818, 1919, 2020, 2121, 2222, 
# 2323, 2424, 2525, 2626, 2727, 
#2828, 2929, 3030, 3131, 3232, 
#3333, 3434, 3535, 3636, 3737, 
#3838, 3939, 4040, 4141, 4242

