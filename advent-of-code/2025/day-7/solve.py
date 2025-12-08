with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def part1():
# key is row #, val is list of col index where there is a beam
    zero = set()
    zero.add(lines[0].index('S'))
    beam_indices = {0: zero}
    splits = 0
    for i, line in enumerate(lines):
        if i == 0:
            continue
        prev_beams = beam_indices[i-1]
        current_beams = set()
        for beam_index in prev_beams:
            if line[beam_index] == '^':
                splits += 1
                current_beams.add(beam_index-1)
                current_beams.add(beam_index+1)
            else:
                current_beams.add(beam_index)
        beam_indices[i] = current_beams

    print(beam_indices)
    print(splits)

def find_val(row, col, cache):
    if row == len(lines)-1:
        cache[(row, col)] = 1
        return

    if lines[row+1][col] == '^':
        if (row+1, col-1) not in cache:
            find_val(row+1, col-1, cache)
        if (row+1, col+1) not in cache:
            find_val(row+1, col+1, cache)
        cache[(row, col)] = cache[(row+1, col-1)] + cache[(row+1, col+1)]
    else:
        find_val(row+1, col, cache)
        cache[(row, col)] = cache[(row+1, col)]
    return

def part2():
    # holds (row, col): count
    cache = {}
    find_val(0, lines[0].index('S'), cache)
    print(cache[(0, lines[0].index('S'))])

def naivePart2():
    beams = [(0, lines[0].index('S'))]
    total = 0
    while len(beams) > 0:
        row, col = beams.pop()
        if row == len(lines)-1:
            total += 1
        else:
            if lines[row+1][col] == '^':
                beams.append((row+1, col-1))
                beams.append((row+1, col+1))
            else:
                beams.append((row+1, col))


part2()
