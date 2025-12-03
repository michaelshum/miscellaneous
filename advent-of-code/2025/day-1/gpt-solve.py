import sys


def count_zeros_method2(moves, modulo=100, start=50):
    """
    Count how many *clicks* land on 0 using method 0x434C49434B.
    moves: iterable of (direction, distance) like ('L', 68)
    modulo: size of dial (0..modulo-1)
    start: starting position
    """
    pos = start
    zeros = 0

    for direction, dist in moves:
        if direction == 'R':
            delta = 1
            # First k where (pos + k) % modulo == 0
            k0 = (modulo - pos) % modulo
        elif direction == 'L':
            delta = -1
            # First k where (pos - k) % modulo == 0
            k0 = pos % modulo
        else:
            raise ValueError(f"Invalid direction: {direction}")

        # If starting already at 0, the *first* hit happens after 100 clicks
        if k0 == 0:
            k0 = modulo

        # If first hit is within this move, count all hits during this move
        if k0 <= dist:
            zeros += 1 + (dist - k0) // modulo

        # Update position after full rotation
        pos = (pos + delta * dist) % modulo
        print(direction + str(dist), pos, zeros)

    return zeros


def parse_moves(file_obj):
    """Parse lines like 'L68' into list of (dir, distance)."""
    moves = []
    for line in file_obj:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])
        moves.append((direction, distance))
    return moves


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve.py <input-file>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        moves = parse_moves(f)

    # Part 2 answer: method 0x434C49434B
    part2_answer = count_zeros_method2(moves)
    print(part2_answer)


if __name__ == "__main__":
    main()

