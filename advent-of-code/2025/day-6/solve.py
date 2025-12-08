import math
with open("small.txt") as file:
    lines = [line.split() for line in file]

def part1():
    sums = []
    for i in range(len(lines[0])):
        sums.append([])
    for i, line in enumerate(lines):
        for index, num in enumerate(line):
            if i == len(lines)-1:
                sums[index].append(num)
            else:
                sums[index].append(int(num))

    total = 0
    for s in sums:
        nums = [int(val) for val in s[:-1]]
        operator = s[-1]
        if operator == '+':
            total += sum(nums)
        elif operator == '*':
            total += math.prod(nums)

    print(total)

with open("input.txt") as file:
    raw_lines = [line[:-1] for line in file]

from pprint import pprint
pprint(raw_lines)

def combine(vals, operator):
    total = 0
    nums = [int(val) for val in vals]
    if operator == '+':
        total += sum(nums)
    elif operator == '*':
        total += math.prod(nums)

    return total

def part2():
    indices = []
    operators = []
    for i, val in enumerate(raw_lines[-1]):
        if val != ' ' and val != '\n':
            indices.append(i)
            operators.append(val)
    print(operators)

    padded_lines = []
    for i in range(len(lines[0])):
        padded_lines.append([])

    range_indices = []
    for i, index in enumerate(indices):
        if i != len(indices)-1:
            range_indices.append((index, indices[i+1]))
        else:
            range_indices.append((index, len(raw_lines[0])+1))
    print(range_indices)

    sums = []
    for line in range(len(range_indices)):
        sums.append([])
    for i, line in enumerate(raw_lines[:-1]):
        for index, (start, end) in enumerate(range_indices):
            val = line[start:end-1]
            sums[index].append(val)

    print(sums)
    total = 0
    for i, s in enumerate(sums):
        out_nums = []
        for ind in range(len(s[0])):
            out_nums.append('')
        for index in range(len(s[0])):
            for num in s:
                out_nums[index] += num[index]
        print(out_nums, operators[i])
        total += combine(out_nums, operators[i])

    print(total)



part2()
