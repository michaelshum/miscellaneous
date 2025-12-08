#https://www.reddit.com/r/adventofcode/comments/zkc974/python_data_structures_for_2d_grids/

with open("small.txt") as file:
    lines = [line.rstrip() for line in file]

grid = {x + 1j * y: val for y, line in enumerate(lines) for x, val in enumerate(line)}
inc = {x + 1j * y: 0 for y, line in enumerate(lines) for x, val in enumerate(line)}
print(grid)

def neighbors(grid, pos):
    candidates = [pos + 1, pos - 1, pos + 1j, pos-1j]
    return [p for p in candidates if p in grid]

def check_nw_diag(grid, pos):
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
for pos in grid.keys():
    print(pos, pos.real, pos.imag)
    x, y = pos
    print(x, y)

#print(list(output.values()).count(2))
