with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

zero_count = 0

current_count = 50
for line in lines:
    direction = line[0]
    magnitude = int(line[1:])
    if direction == "L":
        temp_count = current_count - magnitude
        current_count = temp_count % 100
    elif direction == "R":
        temp_count = current_count + magnitude
        current_count = temp_count % 100
    if current_count == 0:
        zero_count += 1
print(zero_count)
