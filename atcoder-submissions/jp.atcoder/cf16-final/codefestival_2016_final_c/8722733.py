import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def main():
    n, m = map(int, sys.stdin.readline().split())
    can_speak = [[] for _ in range(m + 1)]
    for i in range(n):
        *languages, = map(int, sys.stdin.readline().split())
        for l in languages[1:]:
            can_speak[l].append(i)

    G = [[0] * n for _ in range(n)]

    for language in can_speak:
        for j in range(len(language) - 1):
            G[language[j]][language[j+1]] = 1
            G[language[j+1]][language[j]] = 1

    shortest_path = dijkstra(csgraph=csr_matrix(G), directed=False, indices=0)

    if np.any(shortest_path == np.inf):
        ans = 'NO'
    else:
        ans = 'YES'
    print(ans)

if __name__ == '__main__':
    main()
