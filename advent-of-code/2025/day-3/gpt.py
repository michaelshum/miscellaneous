def max_joltage_for_bank(bank: str) -> int:
    """
    Given a string of digits like '987654321111111',
    return the maximum possible two-digit joltage (keeping order).
    """
    bank = bank.strip()
    # First digit is the only possible tens digit at the start
    best_tens = int(bank[0])
    best_pair = -1

    # Walk through remaining digits as possible ones digits
    for ch in bank[1:]:
        d = int(ch)

        # Use best tens digit seen so far with current ones digit
        pair = 10 * best_tens + d
        if pair > best_pair:
            best_pair = pair

        # Update best tens digit if current digit is larger
        if d > best_tens:
            best_tens = d

    return best_pair


def total_output_joltage(lines):
    """
    Sum the max joltage from each non-empty bank line.
    """
    for line in lines:
        print(line, max_joltage_for_bank(line))
    return sum(max_joltage_for_bank(line) for line in lines if line.strip())


with open("input.txt") as f:
    lines = f.readlines()
print(total_output_joltage(lines))
