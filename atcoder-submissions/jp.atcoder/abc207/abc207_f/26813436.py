import sys
import typing

import numba as nb
import numpy as np


@nb.njit
def csgraph_to_directed(g: np.ndarray) -> np.ndarray:
    m = len(g)
    g = np.vstack((g, g))
    g[m:, :2] = g[m:, 1::-1]
    return g


@nb.njit
def sort_csgraph(n: int, g: np.ndarray) -> typing.Tuple[(np.ndarray, ) * 3]:
    idx = g[:, 0] << 30 | g[:, 1]
    sort_idx = np.argsort(idx, kind='mergesort')
    g = g[sort_idx]
    original_idx = np.arange(len(g))[sort_idx]
    edge_idx = np.searchsorted(g[:, 0], np.arange(n + 1))
    return g, edge_idx, original_idx


@nb.njit
def euler_tour_edge(
    g: np.ndarray,
    edge_idx: np.ndarray,
    root: int,
) -> typing.Tuple[(np.ndarray, ) * 3]:
    n = 1 if len(g) == 0 else g[:, :2].max() + 1
    parent = np.full(n, -1, np.int64)
    depth = np.zeros(n, np.int64)
    tour = np.empty(n << 1, np.int64)
    st = [root]
    for i in range(n << 1):
        u = st.pop()
        tour[i] = u
        if u < 0: continue
        st.append(~u)
        for v in g[edge_idx[u]:edge_idx[u + 1], 1][::-1]:
            if v == parent[u]: continue
            parent[v] = u
            depth[v] = depth[u] + 1
            st.append(v)
    return tour, parent, depth


@nb.njit((nb.i8[:, :], ), cache=True)
def solve(uv: np.ndarray) -> typing.NoReturn:
    n = len(uv) + 1
    g, edge_idx, _ = sort_csgraph(n, csgraph_to_directed(uv))
    mod = 10 ** 9 + 7

    dp = np.zeros((n, n + 1, 3), np.int64)
    tour, parent, _ = euler_tour_edge(g, edge_idx, 0)
    size = np.ones(n, np.int64)
    for u in tour:
        if u >= 0: continue
        u = ~u
        dp[u, 0, 0] = dp[u, 1, 2] = 1
        for v in g[edge_idx[u]:edge_idx[u + 1], 1]:
            if v == parent[u]: continue
            ndp = np.zeros((n + 1, 3), np.int64)
            for ui in range(size[u] + 1):
                for vi in range(size[v] + 1):
                    i = ui + vi
                    ndp[i, 0] += dp[u, ui, 0] * dp[v, vi, :2].sum() % mod
                    ndp[i, 1] += dp[u, ui, 1] * dp[v, vi].sum() % mod
                    ndp[i, 2] += dp[u, ui, 2] * dp[v, vi, 1:].sum() % mod
                    if i < n:
                        ndp[i + 1, 1] += dp[u, ui, 0] * dp[v, vi, 2] % mod
                        ndp[i + 1, 2] += dp[u, ui, 2] * dp[v, vi, 0] % mod
            size[u] += size[v]
            dp[u] = ndp % mod

    for k in range(n + 1):
        print(dp[0, k].sum() % mod)


def main() -> typing.NoReturn:
    n = int(input())
    uv = np.array(sys.stdin.read().split(), dtype=np.int64).reshape(n - 1, 2) - 1
    solve(uv)

main()
