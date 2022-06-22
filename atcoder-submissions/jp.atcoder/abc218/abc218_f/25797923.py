import heapq
import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:, :], ), cache=True)
def csgraph_is_sorted(csgraph: np.ndarray) -> bool:
  return np.all(csgraph[:-1, 0] <= csgraph[1:, 0])


@nb.njit((nb.i8, nb.i8[:, :], ), cache=True)
def sort_csgraph(
  n: int,
  csgraph: np.ndarray,
) -> typing.Tuple[
  np.ndarray,
  np.ndarray,
  np.ndarray,
]:
  sort_idx = np.argsort(csgraph[:, 0], kind='mergesort')
  csgraph = csgraph[sort_idx]
  edge_idx = np.searchsorted(csgraph[:, 0], np.arange(n + 1))
  original_idx = np.arange(len(csgraph))[sort_idx]
  return csgraph, edge_idx, original_idx


@nb.njit((nb.i8, nb.i8[:, :], nb.i8[:], nb.i8), cache=True)
def shortest_path_bfs(
  n: int,
  csgraph: np.ndarray,
  edge_idx: np.ndarray,
  src: int,
) -> np.ndarray:
  assert csgraph.shape == (len(csgraph), 2)
  inf = 1 << 60
  assert csgraph_is_sorted(csgraph)
  predecessor = np.full(n, -1, np.int64)
  dist = np.full(n, inf, np.int64)
  dist[src] = 0
  fifo_q = [0]
  for u in fifo_q:
    for i in range(edge_idx[u], edge_idx[u + 1]):
      v = csgraph[i, 1]
      dv = dist[u] + 1
      if dv >= dist[v]: continue
      dist[v] = dv
      predecessor[v] = u
      fifo_q.append(v)
  return predecessor



@nb.njit((nb.i8, nb.i8[:, :], nb.i8[:], nb.i8), cache=True)
def shortest_dist_bfs(
  n: int,
  csgraph: np.ndarray,
  edge_idx: np.ndarray,
  src: int,
) -> np.ndarray:
  assert csgraph.shape == (len(csgraph), 2)
  inf = 1 << 60
  assert csgraph_is_sorted(csgraph)
  dist = np.full(n, inf, np.int64)
  dist[src] = 0
  fifo_q = [0]
  for u in fifo_q:
    for i in range(edge_idx[u], edge_idx[u + 1]):
      v = csgraph[i, 1]
      dv = dist[u] + 1
      if dv >= dist[v]: continue
      dist[v] = dv
      fifo_q.append(v)
  return dist



@nb.njit((nb.i8, nb.i8[:, :]), cache=True)
def solve(
  n: int,
  st: np.ndarray,
) -> typing.NoReturn:
  m = len(st)
  st, edge_idx, original_idx = sort_csgraph(n, st)

  predecessor = shortest_path_bfs(n, st, edge_idx, 0)

  def retrieve_used_edges():
    used_edges = np.empty(n - 1, np.int64)
    idx_to_add = 0
    def add_edge(i):
      nonlocal idx_to_add
      used_edges[idx_to_add] = i
      idx_to_add += 1
    pre = n - 1
    for _ in range(n - 1):
      pre, to = predecessor[pre], pre
      if pre == -1: break
      for i in range(edge_idx[pre], edge_idx[pre + 1]):
        if st[i, 1] != to: continue
        add_edge(i)
        break
    return used_edges[:idx_to_add]

  used_edges = retrieve_used_edges()

  dist = shortest_dist_bfs(n, st, edge_idx, 0)
  res = np.full(m, dist[-1], np.int64)

  for i in used_edges:
    g = st[np.arange(m) != i]
    u = st[i, 0]
    edge_idx[u + 1:] -= 1
    res[i] = shortest_dist_bfs(n, g, edge_idx, 0)[-1]
    edge_idx[u + 1:] += 1

  inf = 1 << 60
  res[res == inf] = -1
  ans = np.empty(m, np.int64)
  ans[original_idx] = res
  for d in ans:
    print(d)



def main() -> typing.NoReturn:
  n, m = map(int, input().split())
  st = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(m, 2) - 1
  solve(n, st)




main()
