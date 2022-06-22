import sys
import typing

import numba as nb
import numpy as np


@nb.njit(
  (nb.i8, nb.i8[:]),
  cache=True,
)
def solve(
  k: int,
  a: np.array,
) -> typing.NoReturn:
  win = np.zeros(
    k + 1,
    dtype=np.bool8,
  )
  for i in range(k):
    for x in a:
      if i + x > k: continue
      win[i + x] |= ~win[i]

  print(
    'First' if win[k]
    else 'Second',
  )


def main() -> typing.NoReturn:
  n, k = map(
    int, input().split(),
  )
  a = np.array(
    sys.stdin.readline()
    .split(),
    dtype=np.int64,
  )
  solve(k, a)


main()
