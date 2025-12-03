import math, sys
with open(sys.argv[1]) as file:
    lines = [line.rstrip() for line in file]

zero_count = 0

def count_zeros(start_value, direction, magnitude):
    global zero_count
    if direction == 'L':
        final_value = start_value - magnitude
    else:
        final_value = start_value + magnitude

    if final_value > start_value:
        zero_count += math.floor(final_value/100)
    elif final_value < start_value and final_value < 0:
        positive = start_value - magnitude
        if start_value > 0:
            zero_count += 1
        zero_count += math.floor(abs(positive)/100)
    elif final_value == 0:
        zero_count += 1
    return final_value % 100

# count number of times we cross 100
count = 50
for line in lines:
    direction = line[0]
    magnitude = int(line[1:])
    old_count = count
    count = count_zeros(count, direction, magnitude)
    print(line, old_count, count, zero_count)

print(zero_count)
