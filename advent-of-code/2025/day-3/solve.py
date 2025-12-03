with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def find_max(batteries):
    return max(batteries)

def part1():
    total = 0
    for line in lines:
        top = find_max(line[:-1])
        index = line.index(top)
        second = find_max(line[index+1:])
        value = int(top) * 10 + int(second)
        total += value
    print(total)

def part2():
    total = 0
    for line in lines:
        level = line
        index = 0
        value = 0
        for i in range(11, -1, -1):
            if len(level) == 1:
                value += int(level[0])
            elif i == 0:
                value += int(find_max(level))
            else:
                if len(level[0:-1]) == 0:
                    import pdb; pdb.set_trace()
                top = find_max(level[0:-i])
                index = level.index(top)
                level = level[index+1:]
                value += int(top) * 10**i
        total += value
    print(total)
part2()
