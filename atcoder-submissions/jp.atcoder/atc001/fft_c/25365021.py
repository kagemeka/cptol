import sys
import typing

import numpy as np


def solve(
  a: np.array,
  b: np.array,
) -> typing.NoReturn:
  a = np.pad(a, (1, 0))
  b = np.pad(b, (1, 0))
  c = np.convolve(a, b)
  print(*c[1:], sep='\n')


def main() -> typing.NoReturn:
  n = int(input())
  a, b = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(n, 2).T
  solve(a, b)



main()
