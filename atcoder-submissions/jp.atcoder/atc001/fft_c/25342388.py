import sys
import typing

import numpy as np


def solve(
  a: np.array,
  b: np.array,
) -> typing.NoReturn:
  n = a.size
  m = 1 << 18
  a = np.pad(a, (1, 0))
  b = np.pad(b, (1, 0))
  a = np.fft.rfft(a, m)
  b = np.fft.rfft(b, m)
  c = a * b
  c = np.fft.irfft(c)
  c = np.real(c)
  c = np.round(c).astype(int)
  print(*c[1:2 * n + 1], sep='\n')


def main() -> typing.NoReturn:
  n = int(input())
  a, b = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(n, 2).T
  solve(a, b)



main()
