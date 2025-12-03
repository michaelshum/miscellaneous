def is_valid_part1(number):
    """
    Checks if a number is composed of a sequence repeated exactly twice.
    Example: 123123 (True), 121212 (False - 3 times), 101 (False)
    """
    s = str(number)
    length = len(s)
    
    # Must be even length to be split exactly in two
    if length % 2 != 0:
        return False
    
    mid = length // 2
    return s[:mid] == s[mid:]

def is_valid_part2(number):
    """
    Checks if a number is composed of a sequence repeated at least twice.
    Example: 123123 (True), 111 (True), 1212 (True)
    """
    s = str(number)
    length = len(s)
    
    # Try all possible pattern lengths from 1 up to half the string's length
    # We stop at length//2 because a pattern must repeat at least twice
    for pattern_len in range(1, (length // 2) + 1):
        # The total length must be divisible by the pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            multiplier = length // pattern_len
            
            # Reconstruct the string using the pattern
            if pattern * multiplier == s:
                return True
                
    return False

def solve_puzzle():
    try:
        with open("input.txt") as file:
            file_string = [line.rstrip() for line in file]
            range_string = file_string[0]
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Please create the file with the input string.")
        return

    # Parse the ranges from "11-22,95-115,..." format
    ranges = []
    raw_ranges = range_string.split(',')
    
    for r in raw_ranges:
        start_str, end_str = r.split('-')
        ranges.append((int(start_str), int(end_str)))

    part1_sum = 0
    part2_sum = 0

    # Iterate through the parsed ranges
    for start, end in ranges:
        # Range is inclusive for start and end
        for num in range(start, end + 1):
            if is_valid_part1(num):
                part1_sum += num
            
            if is_valid_part2(num):
                part2_sum += num

    print(f"--- Results ---")
    print(f"Part 1 Sum (Repeated exactly twice): {part1_sum}")
    print(f"Part 2 Sum (Repeated at least twice): {part2_sum}")

if __name__ == "__main__":
    solve_puzzle()
