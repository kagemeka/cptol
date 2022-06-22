import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:], nb.i8), cache=True)
def solve(
  a: np.ndarray,
  k: int,
) -> typing.NoReturn:
  n = len(a)


  def possible(x):
    cnt = 0
    for i in range(n):
      cnt += (a[i] + x - 1) // x - 1
    return cnt <= k


  def binary_search():
    lo, hi = 0, 1 << 30
    while hi - lo > 1:
      x = (lo + hi) // 2
      if possible(x):
        hi = x
      else:
        lo = x
    return hi

  print(binary_search())



def main() -> typing.NoReturn:
  n, k = map(int, input().split())
  a = np.array(
    sys.stdin.readline().split(),
    dtype=np.int64,
  )
  solve(a, k)


main()
