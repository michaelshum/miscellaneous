from pprint import pprint
with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

output = {}

def check_nw_diag(row_index, col_index):
    if row_index < 2 or col_index < 2:
        return False
    return lines[row_index-1][col_index-1] == 'A' and lines[row_index-2][col_index-2] == 'S'

def check_ne_diag(row_index, col_index):
    if row_index < 2 or col_index > len(lines[0]) - 3:
        return False
    return lines[row_index-1][col_index+1] == 'A' and lines[row_index-2][col_index+2] == 'S'

def check_sw_diag(row_index, col_index):
    if row_index > len(lines) - 3 or col_index < 2:
        return False
    return lines[row_index+1][col_index-1] == 'A' and lines[row_index+2][col_index-2] == 'S'

def check_se_diag(row_index, col_index):
    if row_index > len(lines) - 3 or col_index > len(lines[0]) - 3:
        return False
    return lines[row_index+1][col_index+1] == 'A' and lines[row_index+2][col_index+2] == 'S'

def add_A(row_index, col_index):
    if (row_index, col_index) not in output:
        output[(row_index, col_index)] = 0
    output[(row_index, col_index)] += 1

total = 0
for row_index, line in enumerate(lines):
    for col_index, char in enumerate(line):
        if char == 'M':
            if check_nw_diag(row_index, col_index):
                add_A(row_index-1, col_index-1)
            if check_ne_diag(row_index, col_index):
                add_A(row_index-1, col_index+1)
            if check_sw_diag(row_index, col_index):
                add_A(row_index+1, col_index-1)
            if check_se_diag(row_index, col_index):
                add_A(row_index+1, col_index+1)

print(list(output.values()).count(2))
