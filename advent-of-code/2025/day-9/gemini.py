import numpy as np

def solve_movie_theater_part2():
    filename = 'input.txt'
    
    # Read and parse input
    try:
        with open(filename, 'r') as f:
            points = []
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    points.append((int(parts[0]), int(parts[1])))
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file is in the current directory.")
        return

    # Convert to numpy array for efficient vectorized operations
    vertices = np.array(points)
    n = len(vertices)
    
    # Pre-calculate polygon edges
    # p_start[i] connects to p_end[i]
    p_start = vertices
    p_end = np.roll(vertices, -1, axis=0)

    # Identify vertical and horizontal edges for intersection checks
    is_vert = p_start[:, 0] == p_end[:, 0]
    
    v_edges_start = p_start[is_vert]
    v_edges_end = p_end[is_vert]
    v_x = v_edges_start[:, 0]
    v_y_min = np.minimum(v_edges_start[:, 1], v_edges_end[:, 1])
    v_y_max = np.maximum(v_edges_start[:, 1], v_edges_end[:, 1])
    
    h_edges_start = p_start[~is_vert]
    h_edges_end = p_end[~is_vert]
    h_y = h_edges_start[:, 1]
    h_x_min = np.minimum(h_edges_start[:, 0], h_edges_end[:, 0])
    h_x_max = np.maximum(h_edges_start[:, 0], h_edges_end[:, 0])

    max_area = 0

    # Iterate through all unique pairs of red tiles
    for i in range(n):
        for j in range(i + 1, n):
            p1 = vertices[i]
            p2 = vertices[j]
            
            # Define candidate rectangle boundaries
            x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            
            # Calculate Area (inclusive of boundary tiles)
            current_area = (x2 - x1 + 1) * (y2 - y1 + 1)
            
            # Optimization: Skip if area isn't larger than what we've found
            if current_area <= max_area:
                continue

            # --- VALIDITY CHECK 1: Center Point ---
            # Check if the geometric center of the rectangle is inside the polygon
            # We use coordinates .5 to avoid hitting edges/vertices exactly
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            
            # Ray Casting Algorithm (cast ray to the right)
            # Find edges that cross the Y-level of our point
            y_cross = (p_start[:, 1] > cy) != (p_end[:, 1] > cy)
            
            # Calculate x-intersection for crossing edges
            # x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            # We select only the relevant edges to compute
            idx_cross = np.where(y_cross)[0]
            ps_c = p_start[idx_cross]
            pe_c = p_end[idx_cross]
            
            intersect_x = ps_c[:, 0] + (cy - ps_c[:, 1]) * (pe_c[:, 0] - ps_c[:, 0]) / (pe_c[:, 1] - ps_c[:, 1])
            
            # Count intersections to the right of cx
            crossings = np.sum(intersect_x > cx)
            
            # Odd crossings = Inside, Even = Outside
            if crossings % 2 == 0:
                continue

            # --- VALIDITY CHECK 2: Edge Intersection ---
            # Even if the center is inside, the rectangle might cross a boundary and go outside.
            # We check if any polygon edge strictly intersects the INTERIOR of the rectangle.
            
            # Vertical edges intersecting interior?
            # x must be strictly between x1 and x2
            # y range must overlap strictly with y1 and y2
            v_x_cond = (v_x > x1) & (v_x < x2)
            v_y_cond = np.maximum(v_y_min, y1) < np.minimum(v_y_max, y2)
            if np.any(v_x_cond & v_y_cond):
                continue
                
            # Horizontal edges intersecting interior?
            # y must be strictly between y1 and y2
            # x range must overlap strictly with x1 and x2
            h_y_cond = (h_y > y1) & (h_y < y2)
            h_x_cond = np.maximum(h_x_min, x1) < np.minimum(h_x_max, x2)
            if np.any(h_y_cond & h_x_cond):
                continue

            # If we pass all checks, this is a valid rectangle
            max_area = current_area

    print(f"Largest valid area: {max_area}")

if __name__ == '__main__':
    solve_movie_theater_part2()
