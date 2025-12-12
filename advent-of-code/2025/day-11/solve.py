with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

# node -> [node, node]
paths = {}

for line in lines:
    split = line.split(":")
    start = split[0]
    nodes = split[1].split()
    paths[start] = nodes

# dfs through to get to out
# assume for now no endless loops
def part1(start, end):
    total = 0
    def walk(node):
        nonlocal total
        if node == end:
            total += 1
            return

        for next_node in paths[node]:
            walk(next_node)

    walk(start)
    print(total)

# part1('you', 'out')
#part1('dac', 'out')

from pprint import pprint

# fft is always before dac in input
# can't search svr to fft, too many branches
# number of paths from svr to fft * number of paths from fft to out (including dac)

# ['fft', 'pxh', 'wgn', 'uot', 'hsw', 'phm', 'tbl', 'kxu', 'ajz', 'mpp', 'skm', 'wsh', 'nkn', 'mze', 'dac', 'odo', 'fpa', 'urb', 'zrh', 'vue', 'fda', 'bck', 'sfx', 'out']

# dfs approach
def part2():
# (node, seen_dac, seen_fft): count of paths to out, if completed
    cache = {}
    def walk(node, seen_dac, seen_fft):

        seen_dac = seen_dac or node == 'dac'
        seen_fft = seen_fft or node == 'fft'

        if (node, seen_dac, seen_fft) in cache:
            return cache[(node, seen_dac, seen_fft)]
        if node == 'out':
            return 1 if seen_dac and seen_fft else 0


        total = 0
        for next_node in paths[node]:
            total += walk(next_node, seen_dac, seen_fft)
        cache[(node, seen_dac, seen_fft)] = total
        return total

    walk('svr', False, False)
    print(cache[('svr', False, False)])
#    walk('dac', ['dac'], 'out',  None)
#
#    walk('svr', ['svr'], 'fft', None)
#    import pdb; pdb.set_trace()
#    print([path for path in all_paths if 'dac' in path])

part2()

