from pprint import pprint
with open("small.txt") as file:
    lines = [line.rstrip() for line in file]

def check_neighbors_for_letter(matrix, search_letter, current_letter, row_index, col_index): 
    above_row = row_index - 1 if row_index > 0 else None
    below_row = row_index + 1 if row_index < len(lines)-1 else None
    left_column = col_index - 1 if col_index > 0 else None
    right_column = col_index + 1 if col_index < len(lines[0])-1 else None

    search_directions = [(above_row, left_column), (above_row, col_index), (above_row, right_column),
    (row_index, left_column), (row_index, right_column),
    (below_row, left_column), (below_row, col_index), (below_row, right_column)]

    filtered_directions = [
        (r, c) for r, c in search_directions
        if r is not None and c is not None
    ]

    for row, col in filtered_directions:
        if lines[row][col] == search_letter and matrix[row][col][search_letter] > 0:
            matrix[row_index][col_index][current_letter] += 1


def part1():
    # matrix holds { M: True, A: False }. represents if this square has a letter AND is next to a valid next letter
    matrix = []
    for line in lines:
        matrix.append([{ 'X': 0, 'M': 0, 'A': 0, 'S': 0 } for _ in line])

    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == 'S':
                matrix[row_index][col_index]['S'] = 1
    # A pass
    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == 'A':
                check_neighbors_for_letter(matrix, 'S', 'A', row_index, col_index)

    # M pass
    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == 'M':
                check_neighbors_for_letter(matrix, 'A', 'M', row_index, col_index)

    # X pass
    for row_index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == 'X':
                check_neighbors_for_letter(matrix, 'M', 'X', row_index, col_index)

    count = 0
    for row in matrix:
        for dic in row:
            if dic['X']:
                count += dic['X']

    pprint(matrix)
    print(count)

part1()
