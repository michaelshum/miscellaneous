with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

split_index = lines.index('')
rules = lines[:split_index]
pages = lines[split_index+1:]

flip_rules = {}
rules_dict = {}
for rule in rules:
    start, end = rule.split("|")
    if start not in rules_dict:
        rules_dict[start] = []
    rules_dict[start].append(end)

    if end not in flip_rules:
        flip_rules[end] = []
    flip_rules[end].append(start)

def is_valid(page_split):
    for val_index, val in enumerate(page_split[:-1]):
        if val in flip_rules:
            before_vals = flip_rules[val]
            for before_val in before_vals:
                if before_val in page_split and page_split.index(before_val) > val_index:
                    return False
    return True

def get_middle(page):
    return page[int(len(page)/2)]

def part1():
    total = 0
    for page in pages:
        page_split = page.split(",")
        if is_valid(page_split):
            total += int(get_middle(page_split))

    print(total)

# for each value, starting from the last one
# find the earliest index that is supposed to be after this value
# move to that index, and update the array
# go to next value
def fix_invalid(page):
    new_page = page[:]
    reverse = page[::-1]
    for val in reverse:
        val_index = new_page.index(val)
        found_indices = []
        for i in range(0, val_index):
            if val in rules_dict and new_page[i] in rules_dict[val]:
                found_indices.append(i)
        if len(found_indices) > 0:
            min_index = min(found_indices)
            update_page = new_page[:min_index] + [val] + new_page[min_index:val_index] + new_page[val_index+1:]
            new_page = update_page
    return int(get_middle(new_page))

def part2():
    invalids = []
    total = 0
    for page in pages:
        page_split = page.split(",")
        if not is_valid(page_split):
            invalids.append(page_split)
    for invalid in invalids:
        total += fix_invalid(invalid)

    print(total)
part2()
