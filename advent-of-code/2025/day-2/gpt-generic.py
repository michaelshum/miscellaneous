import sys
def is_valid_n_times(number, n):
    """
    Checks if a number is composed of a sequence repeated exactly 'n' times.
    
    Args:
        number: The integer or string to check.
        n: The number of times the sequence must be repeated.
    
    Returns:
        True if the number is a sequence repeated n times, False otherwise.
    """
    s = str(number)
    length = len(s)
    
    # If the string length isn't divisible by n, it can't be split evenly n times
    if length % n != 0:
        return False
    
    # Calculate the length of the sub-sequence
    chunk_size = length // n
    
    # Get the pattern (the first chunk)
    pattern = s[:chunk_size]
    
    # Check if repeating that pattern n times equals the original string
    return pattern * n == s

# --- Wrapper specifically for 3 times ---
def is_valid_three_times(number):
    return is_valid_n_times(number, 3)

# --- Example Usage ---
examples = [
    123123123,  # Valid (123 repeated 3 times)
    121212,     # Valid (12 repeated 3 times)
    555,        # Valid (5 repeated 3 times)
    123123,     # Invalid (123 repeated 2 times, not 3)
    12345       # Invalid
]

#print(f"{'Number':<15} | {'Is Repeated 3 Times?'}")
#print("-" * 35)

#for num in examples:
#    result = is_valid_three_times(num)
#    print(f"{num:<15} | {result}")

with open("input.txt") as file:
    file_string = [line.rstrip() for line in file]
    range_string = file_string[0]

ranges = []
raw_ranges = range_string.split(',')
for r in raw_ranges:
    start_str, end_str = r.split('-')
    ranges.append((int(start_str), int(end_str)))

total_sum = 0
n = int(sys.argv[1])  # Change this to whatever n you want to check for

for start, end in ranges:
    for num in range(start, end + 1):
        if is_valid_n_times(num, n):
            total_sum += num

print(f"Sum of IDs repeated exactly {n} times: {total_sum}")
