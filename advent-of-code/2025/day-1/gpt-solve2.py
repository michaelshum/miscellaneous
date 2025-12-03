import sys

MOD = 100  # dial has numbers 0-99


def count_zero_hits_during_rotation(pos, direction, steps):
    """
    Count how many times the dial passes through 0 during a rotation of `steps`
    starting from position `pos` in given `direction` ('L' or 'R').

    We count *clicks* that land on 0, not the initial position.
    """
    if steps <= 0:
        return 0

    if direction == 'R':
        # positions: (pos + s) % 100 for s = 1..steps
        # solve pos + s ≡ 0 (mod 100) -> s ≡ -pos (mod 100)
        residue = (-pos) % MOD
    else:  # 'L'
        # positions: (pos - s) % 100 for s = 1..steps
        # solve pos - s ≡ 0 (mod 100) -> s ≡ pos (mod 100)
        residue = pos % MOD

    # First step s >= 1 where s ≡ residue (mod 100)
    first_step = residue if residue != 0 else MOD

    if first_step > steps:
        return 0

    # After first_step, every +100 steps we hit 0 again
    return 1 + (steps - first_step) // MOD


def parse_line(line):
    line = line.strip()
    if not line:
        return None
    # Support both "L68" and "L 68"
    if " " in line:
        parts = line.split()
        direction = parts[0][0]
        amount = int(parts[1])
    else:
        direction = line[0]
        amount = int(line[1:])
    return direction, amount


def solve(rotations):
    pos = 50
    part1 = 0  # times dial at 0 after a rotation
    part2 = 0  # times any click lands on 0

    for direction, amount in rotations:
        # Part 2: count clicks that land on 0 during this rotation
        part2 += count_zero_hits_during_rotation(pos, direction, amount)

        # Apply rotation to update dial position
        if direction == 'R':
            pos = (pos + amount) % MOD
        else:  # 'L'
            pos = (pos - amount) % MOD

        # Part 1: if dial ends at 0 after this rotation
        if pos == 0:
            part1 += 1

    return part1, part2


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve.py <input_file>")
        sys.exit(1)

    filename = sys.argv[1]

    rotations = []
    with open(filename) as f:
        for line in f:
            parsed = parse_line(line)
            if parsed is not None:
                rotations.append(parsed)

    part1, part2 = solve(rotations)
    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()

