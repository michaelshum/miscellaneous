from pprint import pprint
with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def check_left(row_index, col_index):
    if col_index < 3:
        return False
    else:
        return lines[row_index][col_index-1] == 'M' and lines[row_index][col_index-2] == 'A' and lines[row_index][col_index-3] == 'S'

def check_right(row_index, col_index):
    if col_index > len(lines[0]) - 4:
        return False
    else:
        return lines[row_index][col_index+1] == 'M' and lines[row_index][col_index+2] == 'A' and lines[row_index][col_index+3] == 'S'

def check_top(row_index, col_index):
    if row_index < 3:
        return False
    return lines[row_index-1][col_index] == 'M' and lines[row_index-2][col_index] == 'A' and lines[row_index-3][col_index] == 'S'

def check_bottom(row_index, col_index):
    if row_index > len(lines) - 4:
        return False
    return lines[row_index+1][col_index] == 'M' and lines[row_index+2][col_index] == 'A' and lines[row_index+3][col_index] == 'S'

def check_nw_diag(row_index, col_index):
    if row_index < 3 or col_index < 3:
        return False
    return lines[row_index-1][col_index-1] == 'M' and lines[row_index-2][col_index-2] == 'A' and lines[row_index-3][col_index-3] == 'S'

def check_ne_diag(row_index, col_index):
    if row_index < 3 or col_index > len(lines[0]) - 4:
        return False
    return lines[row_index-1][col_index+1] == 'M' and lines[row_index-2][col_index+2] == 'A' and lines[row_index-3][col_index+3] == 'S'

def check_sw_diag(row_index, col_index):
    if row_index > len(lines) - 4 or col_index < 3:
        return False
    return lines[row_index+1][col_index-1] == 'M' and lines[row_index+2][col_index-2] == 'A' and lines[row_index+3][col_index-3] == 'S'

def check_se_diag(row_index, col_index):
    if row_index > len(lines) - 4 or col_index > len(lines[0]) - 4:
        return False

    return lines[row_index+1][col_index+1] == 'M' and lines[row_index+2][col_index+2] == 'A' and lines[row_index+3][col_index+3] == 'S'

def part1():
    total = 0
    for row_index, line in enumerate(lines):
#        print(line)
        for col_index, char in enumerate(line):
            directions = []
            if char == 'X':
                directions.append(check_left(row_index, col_index))
                directions.append(check_right(row_index, col_index))
                directions.append(check_top(row_index, col_index))
                directions.append(check_bottom(row_index, col_index))
                directions.append(check_nw_diag(row_index, col_index))
                directions.append(check_ne_diag(row_index, col_index))
                directions.append(check_sw_diag(row_index, col_index))
                directions.append(check_se_diag(row_index, col_index))
                total += sum(directions)
#                print(directions, sum(directions))
    print(total)

part1()
