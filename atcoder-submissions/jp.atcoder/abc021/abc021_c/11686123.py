import sys
from collections import deque

inf = float("inf")
MOD = 19**9 + 7

(*I,) = map(int, sys.stdin.read().split())
n = I[0]
a, b = I[1:3]
a -= 1
b -= 1
graph = [[] for _ in range(n)]
for x, y in zip(*[iter(I[4:])] * 2):
    graph[x - 1].append(y - 1)
    graph[y - 1].append(x - 1)


def main():
    dist = [inf] * n
    dist[a] = 0
    paths = [0] * n
    paths[a] = 1
    q = deque([a])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] < dist[u] + 1:
                continue
            if dist[v] == inf:
                q.append(v)
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                paths[v] = paths[u]
            else:
                paths[v] += paths[u]
                paths[v] %= MOD

    print(paths[b])


if __name__ == "__main__":
    main()
