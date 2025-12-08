with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

ranges = []

split_index = lines.index('')
ranges = [[int(x) for x in line.split('-')] for line in lines[:split_index]]
ranges.sort(key=lambda r: r[0])

def part1():
    def find_if_in_ranges(val):
        for low, high in ranges:
            if val >= low and val <= high:
                return True

        return False

    vals = lines[split_index+1:]
    count = 0
    for val in vals:
        if find_if_in_ranges(int(val)):
            count += 1
    print(count)

def part2():
# invariant: merged all overlaps
    new_ranges = []
# walk through all ranges
    for start, end in ranges:
        update_new_ranges = []
        has_updated = False
        print("merging", start, end, new_ranges)
# walk through merged ranges, see if we can merge into any
        for have_start, have_end in new_ranges:
            if has_updated:
                update_new_ranges.append((have_start, have_end))
            elif start<=have_start and end >= have_start and end <= have_end:
                update_new_ranges.append((start, have_end))
                has_updated = True
            elif start <= have_start and end >= have_end:
                update_new_ranges.append((start, end))
                has_updated = True
            elif have_start <= start and have_end >= start and have_end <= end:
                update_new_ranges.append((have_start, end))
                has_updated = True
            elif have_start <= start and have_end >= end:
                update_new_ranges.append((have_start, have_end))
                has_updated = True
            else:
                update_new_ranges.append((have_start, have_end))
        if not has_updated:
            update_new_ranges.append((start, end))
        new_ranges = update_new_ranges
    print(new_ranges)

    total = 0
    for start, end in new_ranges:
        total += (end-start+1)
    print(total)
part2()
