import sys
from heapq import heappop, heappush

import numpy as np

I = np.array(sys.stdin.read().split())
R, C, sy, sx, gy, gx = I[:6].astype(np.int64) - 1
R += 1
C += 1
grid = I[6:]


def main():
    q = []
    heappush(q, (0, sx, sy))
    visited = np.zeros((R, C), dtype=np.int64)

    while q:
        d, y, x = heappop(q)
        visited[y][x] ^= 1
        if y == gy and x == gx:
            print(d)
            sys.exit()
        for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            i = y + dy
            j = x + dx
            if grid[i][j] == "#":
                continue
            if visited[i][j]:
                continue
            heappush(q, (d + 1, i, j))


if __name__ == "__main__":
    main()

# Dijkstra
