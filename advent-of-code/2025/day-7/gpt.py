with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def part2():
    H = len(lines)
    W = len(lines[0])

    # Find the starting position S
    S_row = S_col = None
    for r, row in enumerate(lines):
        c = row.find('S')
        if c != -1:
            S_row, S_col = r, c
            break

    if S_row is None:
        raise ValueError("No S found in input")

    # ways[c] = number of timelines with the particle just *below* row (r-1)
    # at column c, i.e. entering row r from above.
    # We start just below S, in the same column.
    ways = [0] * W
    if S_row + 1 >= H:
        # S on the bottom row -> the particle immediately exits: 1 timeline
        print(1)
        return

    ways[S_col] = 1

    # Process each row from just below S down to the bottom
    for r in range(S_row + 1, H):
        new_ways = [0] * W
        row = lines[r]

        for c, w in enumerate(ways):
            if w == 0:
                continue

            cell = row[c]

            if cell == '^':
                # Splitter: each incoming timeline branches left and right
                if c > 0:
                    new_ways[c - 1] += w
                if c < W - 1:
                    new_ways[c + 1] += w
            else:
                # Empty (or S, but that won't happen below the first row of S):
                # particle just continues straight down
                new_ways[c] += w

        ways = new_ways

    # After the last row, each remaining beam corresponds to
    # a completed timeline that exits the manifold.
    total_timelines = sum(ways)
    print(total_timelines)
    return total_timelines

part2()
