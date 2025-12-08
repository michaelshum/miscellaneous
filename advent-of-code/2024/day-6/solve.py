with open("small.txt") as file:
    lines = [line.rstrip() for line in file]

# x is x axis
# y is y axis
grid = {x + 1j * y: val for y, line in enumerate(lines) for x, val in enumerate(line)}
print(grid)

# returns is_done, new position, total count
def left(pos, count):
    candidates = [pos - i for i in range(1, int(pos.real) + 1)]
    for c in candidates:
        if grid[c] == '#':
            return (False, c + 1, count, "up")
        count += 1
    return (True, pos, count, "up")

def up(pos, count):
    candidates = [pos - i * 1j for i in range(1, int(pos.imag) + 1)]
    for c in candidates:
        if grid[c] == '#':
            return (False, c + 1j, count, "right")
        count += 1
    return (True, pos, count, "right")

def right(pos, count):
    candidates = [pos + i * 1 for i in range(1, len(lines) - int(pos.real))]
    for c in candidates:
        if grid[c] == '#':
            return (False, c - 1, count, "down")
        count += 1
    return (True, pos, count, "down")

def down(pos, count):
    candidates = [pos + i * 1j for i in range(1, len(lines[0]) - int(pos.imag))]
    for c in candidates:
        if grid[c] == '#':
            return (False, c - 1j, count, "left")
        count += 1
    return (True, pos, count, "left")


pos = next(k for k, v in grid.items() if v == '^')
is_done = False
count = 0
direction = "up"
while not is_done:
    if direction == "left":
        is_done, pos, count, direction = left(pos, count)
    elif direction == "up":
        is_done, pos, count, direction = up(pos, count)
    elif direction == "right":
        is_done, pos, count, direction = right(pos, count)
    elif direction == "down":
        is_done, pos, count, direction = down(pos, count)

print(count)

