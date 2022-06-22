import sys
import typing

import numba as nb
import numpy as np


@nb.njit
def sort_csgraph(
  n: int,
  g: np.ndarray,
) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
  sort_idx = np.argsort(g[:, 0], kind='mergesort')
  g = g[sort_idx]
  edge_idx = np.searchsorted(g[:, 0], np.arange(n + 1))
  original_idx = np.arange(len(g))[sort_idx]
  return g, edge_idx , original_idx


@nb.njit
def scc(n: int, g: np.ndarray) -> np.ndarray:
  # def _scc_dfs(n, g):
  #   g, edge_idx, _ = sort_csgraph(n, g)
  #   order = np.empty(n, np.int64)
  #   ptr = 0
  #   flg = np.zeros(n, np.int8)
  #   for i in range(n):
  #     if flg[i]: continue
  #     st = [i]
  #     flg[i] = 1
  #     while st:
  #       u = st.pop()
  #       if flg[u] == 2:
  #         order[ptr] = u
  #         ptr += 1
  #         continue
  #       flg[u] += 1
  #       st.append(u)
  #       for v in g[edge_idx[u]:edge_idx[u + 1], 1][::-1]:
  #         if flg[v]: continue
  #         flg[v] += 1
  #         st.append(v)
  #   print(order)
  #   return order[::-1]

  def _scc_dfs(n, g):
    g, edge_idx, _ = sort_csgraph(n, g)
    order = np.full(n, -1, np.int64)
    ord_ = 0
    visited = np.zeros(n, np.int8)
    for i in range(n):
      if visited[i]: continue
      st = [i]
      while st:
        u = st.pop()
        if u < 0:
          u = -u - 1
          order[u] = ord_
          ord_ += 1
          continue
        if visited[u]: continue
        visited[u] = True
        st.append(-u - 1)
        for v in g[edge_idx[u]:edge_idx[u + 1], 1][::-1]:
          if visited[v]: continue
          st.append(v)
    que = np.empty(n, np.int64)
    que[order] = np.arange(n)
    return que[::-1]


  def _scc_reverse_dfs(n, g, que):
    g[:, :2] = g[:, 1::-1]
    g, edge_idx, _ = sort_csgraph(n, g)
    label = np.full(n, -1, np.int64)
    l = 0
    for i in que:
      if label[i] != -1: continue
      st = [i]
      label[i] = l
      while st:
        u = st.pop()
        for v in g[edge_idx[u]:edge_idx[u + 1], 1][::-1]:
          if label[v] != -1: continue
          label[v] = l
          st.append(v)
      l += 1
    return label

  g = g.copy()
  que = _scc_dfs(n, g)
  return _scc_reverse_dfs(n, g, que)


@nb.njit((nb.i8, nb.i8[:, :]), cache=True)
def solve(n: int, g: np.ndarray) -> typing.NoReturn:
  label = scc(n, g)
  b = np.bincount(label)
  cnt = np.sum(b * (b - 1) // 2)
  print(cnt)


def main() -> typing.NoReturn:
  n, m = map(int, input().split())
  ab = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(m, 2) - 1
  solve(n, ab)


main()
