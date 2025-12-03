with open("input.txt") as file:
    lines = [line.rstrip() for line in file]


def part1():

    left_list = []
    right_list = []

    for line in lines:
        first, second = line.split()
        left_list.append(int(first))
        right_list.append(int(second))

    left_list.sort()
    right_list.sort()

    total = 0
    for i in range(len(left_list)):
        total += abs(left_list[i] - right_list[i])

    print(total)

def part2():
    left_list = []
    right_hash = {}
    for line in lines:
        first, second = line.split()
        left_list.append(int(first))
        sec_int = int(second)
        if sec_int not in right_hash:
            right_hash[sec_int] = 0

        right_hash[sec_int] += 1

    left_list.sort()
    print(left_list)
    print(right_hash)
    total = 0
    for val in left_list:
        mult = right_hash[val] if val in right_hash else 0
        total += val * mult
    print(total)

part2()
