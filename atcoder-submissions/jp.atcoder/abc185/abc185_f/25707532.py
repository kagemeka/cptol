import sys
import typing

import numba as nb
import numpy as np


@nb.njit
def fw_build(n: int) -> np.ndarray:
  return np.full(n + 1, 0, np.int64)


@nb.njit
def fw_set(
  fw: np.ndarray,
  i: int,
  x: int,
) -> typing.NoReturn:
  while i < len(fw):
    fw[i] ^= x
    i += i & -i


@nb.njit
def fw_get(
  fw: np.ndarray,
  i: int,
) -> int:
  v = 0
  while i > 0:
    v ^= fw[i]
    i -= i & -i
  return v


@nb.njit
def fw_get_range(
  fw: np.ndarray,
  l: int,
  r: int,
) -> int:
  return fw_get(fw, l - 1) ^ fw_get(fw, r)



@nb.njit(
  (nb.i8[:], nb.i8[:, :]),
  cache=True,
)
def solve(
  a: np.ndarray,
  txy: np.ndarray,
) -> typing.NoReturn:
  n, m = len(a), len(txy)
  fw = fw_build(n)
  for i in range(n):
    fw_set(fw, i + 1, a[i])
  for j in range(m):
    t, x, y = txy[j]
    if t == 1:
      fw_set(fw, x, y)
    else:
      print(fw_get_range(fw, x, y))



def main() -> typing.NoReturn:
  n, q = map(int, input().split())
  a = np.array(
    sys.stdin.readline().split(),
    dtype=np.int64,
  )
  txy = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(q, 3)


  solve(a, txy)


main()
