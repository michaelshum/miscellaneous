from itertools import combinations

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def part1():
    points = []
    for line in lines:
        x, y = [int(val) for val in line.split(",")]
        points.append((x, y))
    pairs = list(combinations(points, 2))

    distances = []
    for pair in pairs:
        (x, y), (x0, y0) = pair
        distance = abs(x-x0+1) * abs(y-y0+1)
        distances.append((pair, distance))

    sorted_distances = sorted(distances, key=lambda x: x[1], reverse=True)
    print(sorted_distances[0])
    # generate all pairs
    # calculate euclidean distance squared
    # sort by val

def part2():
    points = []
    for line in lines:
        x, y = [int(val) for val in line.split(",")]
        points.append((x, y))

    pairs = list(combinations(points, 2))
    distances = []

    walls = list(zip(points, points[1:] + points[:1]))

# within_rectangle logic
# ray tracing - check if we can do a ray to the right
# check for every wall - are the y points bounding current y?
# if so, check if x is to the right of our point
# if sum(count) %2 == 1, then we are inside
    def is_center_within(x, y, x0, y0):
        center_x = int((x+x0)/2)
        center_y = int((y+y0)/2)
        count = 0
        for p0, p1 in walls:
            (px, p0y), (_, p1y) = p0, p1
            min_y = min(p0y, p1y)
            max_y = max(p0y, p1y)
            if center_y > min_y and center_y < max_y and px > center_x:
                count += 1
        return count % 2 == 1

# evaluate if any wall intersects an existing wall
# given four points nw, ne, sw, se
# for every red/green wall:
#   if vertical wall, check if there's an intersection between nw/sw or ne/se walls
#     aka min(x value of my rect) < x of vertical AND max(x value of my rect) > x of vert
#     AND y has some intersection
#   if horizontal wall, check if intersection between nw/ne or sw/se walls
    def intersects(x, y, x0, y0):
        for wall in walls:
            (p0x, p0y), (p1x, p1y) = wall
            rect_min_x, rect_max_x = min(p0x, p1x), max(p0x, p1x)
            rect_min_y, rect_max_y = min(p0y, p1y), max(p0y, p1y)

            is_vertical = p0x == p1x

            my_min_x, my_max_x = min(x, x0), max(x, x0)
            my_min_y, my_max_y = min(y, y0), max(y, y0)

            if is_vertical:
                horizontal_intersect = my_min_x < p0x and p0x < my_max_x
                vertical_bottom_overlap = rect_min_y <= my_min_y and my_min_y < rect_max_y
                vertical_top_overlap = rect_min_y < my_max_y and my_max_y <= rect_max_y
                if horizontal_intersect and (vertical_bottom_overlap or vertical_top_overlap):
                    return True
            else:
                vertical_intersect = my_min_y < p0y and p0y < my_max_y
                horizontal_left_overlap = rect_min_x <= my_min_x and my_min_x < rect_max_x
                horizontal_right_overlap = rect_min_x < my_max_x and my_max_x <= rect_max_x
                if vertical_intersect and (horizontal_left_overlap or horizontal_right_overlap):
                    return True
        return False


# for each pair of points
# calculate the rectangle they could make
# evaluate the center - is it within a red/green rectangle?
# if true, then evaluate if any wall of our rectangle intersects with an existing wall
    for pair in pairs:
        (x, y), (x0, y0) = pair
        center = is_center_within(x, y, x0, y0)
        inter = intersects(x, y, x0, y0)
        if center and not inter:
            distance = (abs(x-x0)+1) * (abs(y-y0)+1)
            distances.append((pair, distance))

    sorted_distances = sorted(distances, key=lambda x: x[1], reverse=True)
    print(sorted_distances[0])

part2()
