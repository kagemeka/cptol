import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:], nb.i8), cache=True)
def solve(a: np.ndarray, x: int) -> typing.NoReturn:
  s = a.cumsum()
  n = len(a)
  q, r = divmod(x, s[-1])

  c = q * n
  if r == 0:
    print(c + 1)
    return
  c += np.searchsorted(s, r, side='right') + 1
  print(c)



def main() -> typing.NoReturn:
  n = int(input())
  a = np.array(
    sys.stdin.readline().split(),
    dtype=np.int64,
  )
  x = int(input())
  solve(a, x)


main()
