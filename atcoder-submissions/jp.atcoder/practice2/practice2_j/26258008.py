import sys
import typing

import numba as nb
import numpy as np


@nb.njit
def bit_length(n: int) -> int:
  l = 0
  while 1 << l <= n: l += 1
  return l


S = typing.TypeVar('S')

@nb.njit
def seg_build(
  op: typing.Callable[[S, S], S],
  e: typing.Callable[[], S],
  a: np.ndarray,
) -> np.ndarray:
  n = 1 << bit_length(len(a) - 1)
  seg = np.empty((n << 1, ) + a.shape[1:], np.int64)
  for i in range(n << 1): seg[i] = e()
  seg[n:n + len(a)] = a.copy()
  for i in range(n - 1, 0, -1):
    seg[i] = op(seg[i << 1], seg[i << 1 | 1])
  return seg


@nb.njit
def seg_set(
  seg: np.ndarray,
  op: typing.Callable[[S, S], S],
  i: int,
  x: S,
) -> typing.NoReturn:
  i += len(seg) >> 1
  seg[i] = x
  while i > 1:
    i >>= 1
    seg[i] = op(seg[i << 1], seg[i << 1 | 1])


@nb.njit
def seg_get(
  seg: np.ndarray,
  op: typing.Callable[[S, S], S],
  e: typing.Callable[[], S],
  l: int,
  r: int,
) -> int:
  n = len(seg) >> 1
  l, r = l + n, r + n
  vl = vr = e()
  while l < r:
    if l & 1:
      vl = op(vl, seg[l])
      l += 1
    if r & 1:
      r -= 1
      vr = op(seg[r], vr)
    l, r = l >> 1, r >> 1
  return op(vl, vr)


@nb.njit
def seg_max_right(
  seg: np.ndarray,
  op: np.ndarray,
  e: np.ndarray,
  is_ok: typing.Callable[[S], bool],
  x: S,
  l: int,
  size: int,
) -> int:
  n = len(seg) >> 1
  assert 0 <= l < size
  i = l + n
  v = e()
  while True:
    i //= i & -i
    if is_ok(op(v, seg[i]), x):
      v = op(v, seg[i])
      i += 1
      if i & -i == i: return size
      continue
    while i < n:
      i <<= 1
      if not is_ok(op(v, seg[i]), x): continue
      v = op(v, seg[i])
      i += 1
    return i - n



S = typing.TypeVar('S')
@nb.njit
def seg_op(a: S, b: S) -> S:
  return max(a, b)


@nb.njit
def seg_e() -> S:
  return -(1 << 60)


@nb.njit
def build_seg(a: np.ndarray) -> np.ndarray:
  return seg_build(seg_op, seg_e, a)


@nb.njit
def set_point_seg(
  seg: np.ndarray,
  i: int,
  x: S,
) -> typing.NoReturn:
  seg_set(seg, seg_op, i, x)


@nb.njit
def get_range_seg(seg: np.ndarray, l: int, r: int) -> S:
  return seg_get(seg, seg_op, seg_e, l, r)


@nb.njit
def csgraph_to_directed(g: np.ndarray) -> np.ndarray:
  m = len(g)
  g = np.vstack((g, g))
  g[m:, :2] = g[m:, 1::-1]
  return g


@nb.njit
def sort_csgraph(
  n: int,
  g: np.ndarray,
) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
  sort_idx = np.argsort(g[:, 0], kind='mergesort')
  g = g[sort_idx]
  edge_idx = np.searchsorted(g[:, 0], np.arange(n + 1))
  original_idx = np.arange(len(g))[sort_idx]
  return g, edge_idx, original_idx


@nb.njit((nb.i8[:], nb.i8[:, :]), cache=True)
def solve(a: np.ndarray, q: np.ndarray) -> typing.NoReturn:
  seg = build_seg(a)
  is_ok = lambda x, mx: x < mx
  for i in range(len(q)):
    t, x, y = q[i]
    if t == 1:
      set_point_seg(seg, x - 1, y)
    elif t == 2:
      print(get_range_seg(seg, x - 1, y))
    elif t == 3:
      i = seg_max_right(
        seg, seg_op, seg_e,
        is_ok, y,
        x - 1, len(a),
      )
      print(i + 1)


def main() -> typing.NoReturn:
  n, q = map(int, input().split())
  a = np.array(
    sys.stdin.readline().split(),
    dtype=np.int64,
  )
  q = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(q, 3)
  solve(a, q)


main()
