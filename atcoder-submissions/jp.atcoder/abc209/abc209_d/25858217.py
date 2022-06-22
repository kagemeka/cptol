import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:, :], ), cache=True)
def csgraph_to_undirected(g: np.ndarray) -> np.ndarray:
  m = len(g)
  g = np.vstack((g, g))
  g[m:, :2] = g[m:, 1::-1]
  return g


@nb.njit((nb.i8, nb.i8[:, :]), cache=True)
def sort_csgraph(
  n: int,
  g: np.ndarray,
) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
  sort_idx = np.argsort(g[:, 0], kind='mergesort')
  g = g[sort_idx]
  original_idx = np.arange(len(g))[sort_idx]
  edge_idx = np.searchsorted(g[:, 0], np.arange(n + 1))
  return g, edge_idx, original_idx




@nb.njit((nb.i8, nb.i8[:, :], nb.i8), cache=True)
def tree_bfs(
  n: int,
  g: np.ndarray,
  root: int,
) -> typing.Tuple[np.ndarray, np.ndarray]:
  assert len(g) == n - 1
  g = csgraph_to_undirected(g)
  g, edge_idx, _ = sort_csgraph(n, g)
  parent = np.full(n, -1, np.int64)
  depth = np.zeros(n, np.int64)
  que = [root]
  for u in que:
    for v in g[edge_idx[u]:edge_idx[u + 1], 1]:
      if v == parent[u]: continue
      parent[v] = u
      depth[v] = depth[u] + 1
      que.append(v)
  return parent, depth


@nb.njit((nb.i8[:, :], nb.i8[:, :]), cache=True)
def solve(
  ab: np.ndarray,
  cd: np.ndarray,
) -> typing.NoReturn:
  n = len(ab) + 1
  q = len(cd)
  _, depth = tree_bfs(n, ab, 0)
  for i in range(q):
    c, d = cd[i]
    if (depth[c] - depth[d]) & 1:
      print('Road')
    else:
      print('Town')



def main() -> typing.NoReturn:
  n, q = map(int, input().split())
  tmp = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(-1, 2) - 1
  ab, cd = tmp[:n - 1], tmp[n - 1:]
  solve(ab, cd)


main()
