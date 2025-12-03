import re
with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def calculate_match(string):
    total = 0
    matches = re.findall(r"mul\((\d+),(\d+)\)", string)
    for match in matches:
        mult = int(match[0]) * int(match[1])
        total += mult
    return total

def part1():
    total = 0
    for line in lines:
        total += calculate_match(line)
    print(total)

def part2():
    total = 0
    calculate_state = True
    for line in lines:
        pattern = r"do\(\)|don't\(\)"
        matches = [(m.group(), m.start()) for m in re.finditer(pattern, line)]
        start_index = 0

        for match in matches:
            if match[0] == "don't()" and calculate_state:
                total += calculate_match(line[start_index:match[1]])
                calculate_state = False
            if match[0] == "do()" and not calculate_state:
                calculate_state = True
                start_index = match[1]
        if calculate_state:
            total += calculate_match(line[start_index:])

part2()
