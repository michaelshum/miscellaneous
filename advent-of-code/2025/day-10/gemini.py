import re
import sys
from fractions import Fraction
from math import ceil, floor, inf

def solve():
    try:
        with open("input.txt") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    total_p1 = 0
    total_p2 = 0

    # We need to track if we failed to solve any machine that might have a solution
    unsolvable_p2_count = 0

    for i, line in enumerate(lines):
        # --- Parsing ---
        d_match = re.search(r'\[(.*?)\]', line)
        if not d_match: continue
        d_str = d_match.group(1)
        # Part 1 Target: Light state
        target_lights = [1 if c == '#' else 0 for c in d_str]
        
        j_match = re.search(r'\{(.*?)\}', line)
        # Part 2 Target: Joltage integers
        target_joltages = [int(x) for x in j_match.group(1).split(',')]
        
        middle = line.split(']')[1].split('{')[0]
        b_matches = re.findall(r'\((.*?)\)', middle)
        buttons = []
        for b in b_matches:
            parts = [int(x) for x in b.split(',') if x.strip()]
            buttons.append(parts)
            
        num_lights = len(target_lights)
        num_joltages = len(target_joltages)
        num_buttons = len(buttons)

        # --- Part 1: Modulo 2 Linear System ---
        A1 = [[0] * num_buttons for _ in range(num_lights)]
        for c, btn in enumerate(buttons):
            for r in btn:
                if r < num_lights:
                    A1[r][c] = 1
        
        p1 = solve_gf2(A1, target_lights)
        if p1 is not None:
            total_p1 += p1

        # --- Part 2: Integer Linear System ---
        # Ax = b, minimize sum(x), x >= 0 integers
        A2 = [[0] * num_buttons for _ in range(num_joltages)]
        for c, btn in enumerate(buttons):
            for r in btn:
                if r < num_joltages:
                    A2[r][c] = 1
        
        p2 = solve_int_linear_robust(A2, target_joltages)
        
        if p2 is not None:
            total_p2 += p2
        else:
            unsolvable_p2_count += 1

    print(f"Part 1: {total_p1}")
    print(f"Part 2: {total_p2}")
    if unsolvable_p2_count > 0:
        print(f"(Note: Could not find integer solutions for {unsolvable_p2_count} machines)")

def solve_gf2(A, b):
    """Gaussian Elimination over GF(2)."""
    rows = len(A)
    cols = len(A[0])
    M = [row[:] + [val] for row, val in zip(A, b)]
    pivots = []
    pivot_row = 0
    
    for c in range(cols):
        if pivot_row >= rows: break
        curr = pivot_row
        while curr < rows and M[curr][c] == 0:
            curr += 1
        if curr < rows:
            M[pivot_row], M[curr] = M[curr], M[pivot_row]
            for i in range(pivot_row + 1, rows):
                if M[i][c] == 1:
                    for j in range(c, cols + 1):
                        M[i][j] ^= M[pivot_row][j]
            pivots.append((pivot_row, c))
            pivot_row += 1
            
    for r in range(pivot_row, rows):
        if M[r][cols] == 1: return None
            
    # Back-substitute
    for i in range(len(pivots)-1, -1, -1):
        r, c = pivots[i]
        for rr in range(r):
            if M[rr][c] == 1:
                for j in range(c, cols+1):
                    M[rr][j] ^= M[r][j]

    # Basis construction
    pivot_indices = {c for r, c in pivots}
    free_indices = [c for c in range(cols) if c not in pivot_indices]
    
    # Particular solution
    x_p = [0] * cols
    for r, c in pivots:
        x_p[c] = M[r][cols]

    # Null space vectors
    null_basis = []
    for f in free_indices:
        vec = [0] * cols
        vec[f] = 1
        for r, c in pivots:
            if M[r][f] == 1:
                vec[c] = 1
        null_basis.append(vec)
        
    # Brute force small null space
    import itertools
    best_w = float('inf')
    for coeffs in itertools.product([0, 1], repeat=len(free_indices)):
        cand = list(x_p)
        for i, co in enumerate(coeffs):
            if co:
                for k in range(cols):
                    cand[k] ^= null_basis[i][k]
        w = sum(cand)
        if w < best_w: best_w = w
            
    return best_w if best_w != float('inf') else None

def solve_int_linear_robust(A, b):
    """
    Solves Ax = b for non-negative integers minimizing sum(x).
    Handles determined and under-determined systems.
    """
    rows = len(A)
    cols = len(A[0])
    
    # Use Fraction for exact RREF
    M = [[Fraction(x) for x in r] + [Fraction(y)] for r, y in zip(A, b)]
    
    pivots = []
    pivot_row = 0
    
    # RREF
    for c in range(cols):
        if pivot_row >= rows: break
        curr = pivot_row
        while curr < rows and M[curr][c] == 0:
            curr += 1
        if curr < rows:
            M[pivot_row], M[curr] = M[curr], M[pivot_row]
            inv = 1 / M[pivot_row][c]
            for j in range(c, cols+1):
                M[pivot_row][j] *= inv
            for i in range(rows):
                if i != pivot_row and M[i][c] != 0:
                    factor = M[i][c]
                    for j in range(c, cols+1):
                        M[i][j] -= factor * M[pivot_row][j]
            pivots.append((pivot_row, c))
            pivot_row += 1
            
    # Consistency check
    for r in range(pivot_row, rows):
        if M[r][cols] != 0: return None
        
    pivot_map = {c: r for r, c in pivots}
    free_cols = [c for c in range(cols) if c not in pivot_map]
    
    # --- Case 1: Determined System ---
    if not free_cols:
        sol = []
        for c in range(cols):
            val = M[pivot_map[c]][cols] if c in pivot_map else Fraction(0)
            if val < 0 or val.denominator != 1: return None
            sol.append(int(val))
        return sum(sol)
        
    # --- Case 2: Under-Determined System ---
    # Solution form: x_i = P_i + sum(N_ij * k_j)
    # where P is particular solution, N is null space, k are free params.
    
    # Construct particular solution (P) and Null space (N)
    P = [Fraction(0)] * cols
    N = [[Fraction(0)] * len(free_cols) for _ in range(cols)]
    
    for i, f_col in enumerate(free_cols):
        # The free variable itself depends on the parameter k_i: x_f = k_i
        N[f_col][i] = Fraction(1)
        
    for p_col, r in pivot_map.items():
        P[p_col] = M[r][cols]
        for i, f_col in enumerate(free_cols):
            # x_p = constant - coeff * x_f
            N[p_col][i] = -M[r][f_col]
            
    # We want to minimize sum(x).
    # sum(x) = sum(P) + sum( sum(N_ij * k_j) )
    #        = Cost_Base + sum( Cost_Coeff_j * k_j )
    cost_base = sum(P)
    cost_coeffs = [sum(N[r][j] for r in range(cols)) for j in range(len(free_cols))]
    
    # Constraints: For all r in [0..cols-1]: P[r] + sum(N[r][j]*k_j) >= 0
    # Also k_j must be integer (since x_f are integers).
    # Actually, all x must be integers. Since inputs are int and we solve linear system,
    # if we pick integer k_j, x will be integer IF coefficients allow.
    # However, N contains Fractions. So we need k_j such that resulting x are integers.
    # But usually in these problems, N_ij are integers or simple fractions.
    # We will search for integer k.
    
    # --- Subcase 2a: 1 Degree of Freedom ---
    if len(free_cols) == 1:
        # P[r] + N[r][0] * k >= 0
        # k must satisfy this for all r.
        k_min = -inf
        k_max = inf
        
        valid_k_exists = True
        
        for r in range(cols):
            a = N[r][0]
            b = P[r]
            # a*k + b >= 0
            if a == 0:
                if b < 0: 
                    valid_k_exists = False; break
            elif a > 0:
                # k >= -b/a
                val = ceil(-b/a)
                if val > k_min: k_min = val
            else: # a < 0
                # k <= -b/a
                val = floor(-b/a)
                if val < k_max: k_max = val
        
        if not valid_k_exists or k_min > k_max:
            return None
            
        # We need integer k in [k_min, k_max].
        # Also need to ensure x is integer?
        # If N contains fractions, we might step k by LCM of denominators?
        # For this puzzle, let's check integers in range. 
        # Since it's minimization, we check boundaries and maybe scan if cost function is flat?
        # Cost is linear in k. Min is at boundary.
        
        best_total = inf
        
        # Check boundaries and a few inner points (just in case of divisibility requirements)
        # Note: if range is infinite, we must look at cost slope.
        # If cost increases with k, pick k_min. If decreases, pick k_max.
        slope = cost_coeffs[0]
        
        candidates = []
        if k_min != -inf: candidates.append(k_min)
        if k_max != inf: candidates.append(k_max)
        
        # If slope is positive, we want smallest k. If negative, largest k.
        # If slope is 0, any k works (pick smallest for stability).
        if slope > 0:
            if k_min == -inf: return None # Unbounded descent
            candidates = [k_min, k_min+1, k_min+2]
        elif slope < 0:
            if k_max == inf: return None
            candidates = [k_max, k_max-1, k_max-2]
        else:
            # Slope 0, check range
            if k_min != -inf: candidates.append(k_min)
            if k_max != inf: candidates.append(k_max)
            
        for k in candidates:
            if k < k_min or k > k_max: continue
            # Calculate full X
            current_x = []
            valid = True
            for r in range(cols):
                val = P[r] + N[r][0] * k
                if val < 0 or val.denominator != 1:
                    valid = False; break
                current_x.append(int(val))
            if valid:
                s = sum(current_x)
                if s < best_total: best_total = s
                
        return best_total if best_total != inf else None

    # --- Subcase 2b: Multi-DOF (General Heuristic) ---
    # With >= 2 free vars, we search "near" the vertices of the feasible region.
    # Vertices are intersections of hyperplanes (x_i = 0).
    # We solve subsystems where we force 'd' variables to be 0 (where d = rank).
    # This is effectively checking Basic Feasible Solutions.
    
    import itertools
    best_total = inf
    
    # We have 'cols' variables. We need to set 'len(free_cols)' of them to 0 or boundaries
    # to find vertices? 
    # Actually, simpler: The minimum of a linear function on a convex polyhedron 
    # is at a vertex. A vertex is defined by n active constraints.
    # Constraints are x_i >= 0.
    # We have 'cols' inequalities. We select 'len(free_cols)' of them to be equality (x_i=0).
    # This determines the free parameters k.
    
    # Try forcing every combination of 'len(free_cols)' variables to 0.
    num_free = len(free_cols)
    from itertools import combinations
    
    # Also add "k=0" as a candidate (the particular solution center)
    candidate_ks = []
    candidate_ks.append([Fraction(0)] * num_free)

    # Find vertices
    # System: P_r + sum(N_rj * k_j) = 0  for r in chosen_indices
    indices = range(cols)
    for forced_zeros in combinations(indices, num_free):
        # Solve linear system for k:
        # Matrix mat * k = -vec
        mat = []
        vec = []
        for r in forced_zeros:
            mat.append([N[r][j] for j in range(num_free)])
            vec.append(-P[r])
            
        # Solve mat * k = vec
        # Using small Gaussian elim for k
        # ... (reuse solver logic or simple inversion for 2x2/3x3)
        try:
            k_sol = solve_small_system(mat, vec)
            if k_sol:
                candidate_ks.append(k_sol)
        except:
            pass
            
    # Check all candidates and their integer neighbors
    # For each float candidate, check floor/ceil neighbors
    
    for k_vec in candidate_ks:
        # It's a vector of Fractions.
        # Generate integer neighbors
        base_ints = [[floor(x), ceil(x)] for x in k_vec]
        
        # product of neighbors
        for k_ints in itertools.product(*base_ints):
            # Check validity
            current_x = []
            valid = True
            for r in range(cols):
                val = P[r]
                for j in range(num_free):
                    val += N[r][j] * k_ints[j]
                
                if val < 0 or val.denominator != 1:
                    valid = False; break
                current_x.append(int(val))
                
            if valid:
                s = sum(current_x)
                if s < best_total: best_total = s

    return best_total if best_total != inf else None

def solve_small_system(A, b):
    # Solves Ax=b for square A. Returns vector or None.
    # A is list of lists, b is list. Elements are Fractions.
    n = len(A)
    M = [row[:] + [val] for row, val in zip(A, b)]
    
    for i in range(n):
        # Pivot
        pivot = i
        while pivot < n and M[pivot][i] == 0: pivot += 1
        if pivot == n: return None # Singular
        M[i], M[pivot] = M[pivot], M[i]
        
        inv = 1 / M[i][i]
        for j in range(i, n+1): M[i][j] *= inv
        
        for r in range(n):
            if r != i:
                f = M[r][i]
                for j in range(i, n+1): M[r][j] -= f * M[i][j]
                
    return [M[i][n] for i in range(n)]

if __name__ == '__main__':
    solve()
