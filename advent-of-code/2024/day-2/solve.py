with open("input.txt") as file:
    lines = [line.rstrip() for line in file]
#    lines = lines[:2]

def is_increasing(level):
    init_val = level[0] 
    for val in level[1:]:
        if val <= init_val or val - init_val > 3:
            return False
        init_val = val
    return True

def is_decreasing(level):
    init_val = level[0]
    for val in level[1:]:
        if val >= init_val or init_val - val > 3:
            return False
        init_val = val
    return True

def part1():
    safe = 0
    for line in lines:
        level = [int(val) for val in line.split()]
        if is_increasing(level) or is_decreasing(level):
            safe += 1

    print(safe)

def part2():
    safe = 0
    for line in lines:
        level = [int(val) for val in line.split()]
        levels = [level]
        for i in range(len(level)):
            levels.append(level[0:i] + level[i+1:])
        level_safe = False
        for temp_level in levels:
            if level_safe:
                continue
            if is_increasing(temp_level) or is_decreasing(temp_level):
                safe += 1
                level_safe = True
                continue
part2()
