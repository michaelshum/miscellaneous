from collections import Counter
from functools import reduce
import operator


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # Path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return  # already in the same circuit

        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def parse_input(path: str):
    points = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    return points


def solve(path: str, num_connections: int) -> int:
    points = parse_input(path)
    n = len(points)

    # Build list of all pairwise distances (squared)
    edges = []
    for i in range(n - 1):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx * dx + dy * dy + dz * dz
            edges.append((dist2, i, j))

    # Sort edges by distance (ascending)
    edges.sort(key=lambda e: e[0])

    uf = UnionFind(n)

    # ✅ Process exactly the first num_connections edges,
    #    even if some don't change the circuits.
    for k in range(min(num_connections, len(edges))):
        _, a, b = edges[k]
        uf.union(a, b)

    # Count circuit sizes
    roots = [uf.find(i) for i in range(n)]
    sizes = list(Counter(roots).values())

    sizes.sort(reverse=True)
    top3 = sizes[:3]
    result = reduce(operator.mul, top3, 1)

    print(result)
    return result


if __name__ == "__main__":
    # Example: small.txt with 10 connections -> should print 40
    solve("small.txt", 10)

    # Real input: 1000 connections
    solve("input.txt", 1000)

