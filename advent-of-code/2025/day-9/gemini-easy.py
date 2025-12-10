import sys

def solve_part2_fast():
    # 1. Parse Input
    points = []
    try:
        with open('input.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    points.append((int(parts[0]), int(parts[1])))
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    n = len(points)
    # These represent the walls of our shape
    # poly_x[i], poly_y[i] is the i-th corner
    poly_x = [p[0] for p in points]
    poly_y = [p[1] for p in points]

    max_area = 0

    # Helper: The "Ghost Test" (Is point (px, py) inside the polygon?)
    def is_inside(px, py):
        # We count how many walls we cross
        collision_count = 0
        
        # Loop through every wall of the polygon
        for i in range(n):
            # Get the two ends of the current wall
            x1, y1 = poly_x[i], poly_y[i]
            x2, y2 = poly_x[(i + 1) % n], poly_y[(i + 1) % n]
            
            # Check if our ray (shooting to the right) crosses this wall
            # 1. The wall must be on both sides of our point vertically (one end above, one below)
            # 2. The intersection must be to the right of our point
            if ((y1 > py) != (y2 > py)):
                # Math to find where the crossing happens
                intersect_x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                if px < intersect_x:
                    collision_count += 1
        
        # Odd collisions = Inside
        return collision_count % 2 == 1

    # Helper: The "Laser Test" (Does a rectangle intersect any polygon edge?)
    def intersects_edge(rx1, rx2, ry1, ry2):
        # We define the rectangle by left, right, top, bottom
        # rx1 = min x, rx2 = max x, etc.
        
        for i in range(n):
            # Polygon edge
            px1, py1 = poly_x[i], poly_y[i]
            px2, py2 = poly_x[(i + 1) % n], poly_y[(i + 1) % n]
            
            # Organize polygon edge coords
            ex1, ex2 = min(px1, px2), max(px1, px2)
            ey1, ey2 = min(py1, py2), max(py1, py2)

            is_vertical_edge = (px1 == px2)
            
            if is_vertical_edge:
                # A vertical wall is dangerous if:
                # 1. It is strictly between the rectangle's Left and Right sides
                # 2. It strictly overlaps the rectangle's Top and Bottom
                if (ex1 > rx1 and ex1 < rx2) and (max(ey1, ry1) < min(ey2, ry2)):
                    return True
            else: # Horizontal edge
                # A horizontal wall is dangerous if:
                # 1. It is strictly between the rectangle's Top and Bottom
                # 2. It strictly overlaps the rectangle's Left and Right sides
                if (ey1 > ry1 and ey1 < ry2) and (max(ex1, rx1) < min(ex2, rx2)):
                    return True
                    
        return False

    # 2. Main Loop: Try every pair of red tiles as corners
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            
            # Determine rectangle bounds
            x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            
            current_area = (x2 - x1 + 1) * (y2 - y1 + 1)
            
            # Optimization: If this area is smaller than our best, don't waste time checking it
            if current_area <= max_area:
                continue
            
            # CHECK 1: Is the center of the rectangle inside the shape?
            # We use the center point (average of coordinates)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            if not is_inside(cx, cy):
                continue
                
            # CHECK 2: Do any walls slice through the rectangle?
            if intersects_edge(x1, x2, y1, y2):
                continue
            
            # If we passed both tests, it's valid!
            max_area = current_area

    print(f"Largest Valid Area: {max_area}")

if __name__ == '__main__':
    solve_part2_fast()
