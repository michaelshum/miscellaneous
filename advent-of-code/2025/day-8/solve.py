import math
from itertools import combinations
from pprint import pprint
with open("small.txt") as file:
    lines = [line.rstrip() for line in file]


# naive solution
def part1():
    boxes = []
    for line in lines:
        x, y, z = [int(val) for val in line.split(',')]
        boxes.append((x, y, z))
# generate all pairs
    pairs = list(combinations(boxes, 2))
# calculate euclidean distance. tuple of (((x,y,z),(x0,y0,z0)), distance)
    distances = []
    for pair in pairs:
        (x, y, z), (x0, y0, z0) = pair
        distance = math.sqrt((x-x0) ** 2 + (y-y0) ** 2 + (z-z0) ** 2)
        distances.append((pair, distance))
# sort by distance, take top 1000
    sorted_distances = sorted(distances, key=lambda x: x[1], reverse=False)[:1000]
    top_distances = [x[0] for x in sorted_distances]

    combine_boxes = set()
    for p0, p1 in top_distances:
        combine_boxes.add(p0)
        combine_boxes.add(p1)

    sorted_boxes = sorted(combine_boxes)
    sets = []
    for p0, p1 in top_distances:
        added = False
        set0_index = None
        set1_index = None
        for i, s in enumerate(sets):
            if p0 in s:
                set0_index = i
            if p1 in s:
                set1_index = i
        if set0_index != None and set1_index == None:
            sets[set0_index].add(p1)
        elif set1_index != None and set0_index == None:
            sets[set1_index].add(p0)
        elif set0_index == None and set1_index == None:
            new_set = set()
            new_set.add(p0)
            new_set.add(p1)
            sets.append(new_set)
        elif set1_index != None and set0_index != None:
            if set1_index != set0_index:
                for val in sets[set0_index]:
                    sets[set1_index].add(val)
                sets.pop(set0_index)
    sorted_sets = sorted(sets, key=lambda x: len(x), reverse=True)[:3]
    lengths = [len(x) for x in sorted_sets]
    print(sorted_sets)
    print(math.prod(lengths))

part1()
