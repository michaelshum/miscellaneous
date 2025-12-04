with open("small.txt") as file:
    lines = [line.rstrip() for line in file]

def get_adjacent(row, col):
    access = []
    top_valid = row > 0
    bottom_valid = row < len(lines)-1
    left_valid = col > 0
    right_valid = col < len(lines[0]) - 1
    #top
    if top_valid:
        access.append(lines[row-1][col] == '@')
    #bottom
    if bottom_valid:
        access.append(lines[row+1][col] == '@')
    #left
    if left_valid:
        access.append(lines[row][col-1] == '@')
#right
    if right_valid:
        access.append(lines[row][col+1] == '@')
#nw
    if top_valid and left_valid:
        access.append(lines[row-1][col-1] == '@')
#ne
    if top_valid and right_valid:
        access.append(lines[row-1][col+1] == '@')
#sw
    if bottom_valid and left_valid:
        access.append(lines[row+1][col-1] == '@')
#se
    if bottom_valid and right_valid:
        access.append(lines[row+1][col+1] == '@')

    return sum(access) < 4

def part1():
    global lines
    total = 0
    cont = True
    while cont:
        test = []
        newLines = []
        for row, line in enumerate(lines):
            newLine = []
            for col, char in enumerate(line):
                if char == '@' and get_adjacent(row, col):
                    newLine.append('x')
                    test.append(get_adjacent(row, col))
                else:
                    newLine.append(char)
            newLines.append(newLine)
        total += sum(test)
        if len(test) == 0:
            cont = False
        else:
            lines = newLines
    print(newLines)
    print(total)

part1()
