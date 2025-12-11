import re
with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

# whole-line pattern: [diagram] (...) (...) {...}
line_pattern = re.compile(r"""
    ^\s*
    \[([.#]+)\]              # 1: light diagram
    \s*
    ((?:\([^)]*\)\s*)+)      # 2: all wiring groups as one big chunk
    \{([^}]*)\}              # 3: joltage list
    \s*$
""", re.VERBOSE)

def parse_line(line: str):
    m = line_pattern.match(line)
    if not m:
        raise ValueError(f"Cannot parse line: {line!r}")

    light_diagram = m.group(1)

    wiring_chunk = m.group(2)
    # find each (...) and split by commas into ints
    wiring_groups = []
    for group in re.findall(r"\(([^)]*)\)", wiring_chunk):
        nums = [int(x) for x in group.split(",") if x.strip() != ""]
        wiring_groups.append(nums)

    joltage_str = m.group(3)
    joltage = [int(x) for x in joltage_str.split(",") if x.strip() != ""]

    return light_diagram, wiring_groups, joltage

# bfs, starting from each node
# build tuples (current_state, steps, current_index)
def walk_graph(diagram, wiring):
    end_state = [True if x == '#' else False for x in diagram]
    start_state = [False for x in diagram]
    found = False
    final = None
    queue = []
    for i in range(len(wiring)):
        queue.append((start_state, [], i))
    while found == False:
        current_state, steps, current_index = queue.pop(0)
        button = wiring[current_index]
        new_steps = steps + [button]
        new_state = [not x if index in button else x for index, x in enumerate(current_state)]
        if new_state == end_state:
            found = True
            final = new_steps
            return True, new_steps

        for i, button in enumerate(wiring):
            queue.append((new_state, new_steps, i))

    return False, 'what'

def part1():
    total = 0
    for line in lines:
        diagram, wiring, joltage = parse_line(line)
        print("starting", diagram, wiring)
        solved, steps = walk_graph(diagram, wiring)
        print('solved', solved, steps)
        if solved:
            total += len(steps)
        else:
            print("what", diagram, wiring)

    print(total)

from collections import deque
# bfs, starting from each node
# build tuples (step_count, current_joltage)
def walk_graph_with_joltage(wiring, joltage):
    found = False
    final = None
    queue = deque()
    queue.append((0, [0 for x in joltage]))
    print(len(queue))

    cache = set()
    while queue:
        step_count, current_joltage = queue.popleft()
        if all([current_joltage[i] == joltage[i] for i in range(len(current_joltage))]):
            return True, step_count
        else:
            for button in wiring:
                new_joltage = [x + 1 if index in button else x for index, x in enumerate(current_joltage)]
                if tuple(new_joltage) in cache:
                    continue
                else:
                    if any([new_joltage[i] > joltage[i] for i in range(len(joltage))]):
                        pass
                    else:
                        cache.add(tuple(new_joltage))
                        queue.append((step_count + 1, new_joltage))

    return False, 'what'



def part2():
    total = 0
    for line in lines:
        diagram, wiring, joltage = parse_line(line)
        print(wiring, joltage)
        solved, steps = walk_graph_with_joltage(wiring, joltage)
        print('solved', solved, steps)
        if solved:
            total += steps
        else:
            print("what", diagram, wiring)

    print(total)
part2()
