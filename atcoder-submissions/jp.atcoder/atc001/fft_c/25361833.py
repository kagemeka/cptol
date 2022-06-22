import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.c16[:], nb.optional(nb.b1)))
def fft(
  a: np.ndarray,
  inverse: bool=False
) -> typing.NoReturn:
  n = a.size
  if n == 1: return
  h = 1
  while 1 << h < n: h += 1
  assert 1 << h == n
  b, c = a[::2].copy(), a[1::2].copy()
  fft(b, inverse)
  fft(c, inverse)
  sign = -1 + 2 * inverse
  zeta = np.exp(sign * 2j * np.pi / n * np.arange(n))
  m = n // 2
  a[:m] = a[m:] = c
  a *= zeta
  a[:m] += b; a[m:] += b
  # return a


@nb.njit((nb.c16[:], ))
def ifft(
  a: np.ndarray,
) -> np.ndarray:
  fft(a, inverse=True)
  a /= a.size



@nb.njit((nb.i8[:], nb.i8[:]))
def convolve(
  a: np.ndarray,
  b: np.ndarray,
) -> np.ndarray:
  n = a.size + b.size - 1
  m = 1
  while m < n: m <<= 1
  na = np.zeros(m, dtype=np.complex128)
  nb = np.zeros(m, dtype=np.complex128)
  na[:a.size] = a
  nb[:b.size] = b
  a, b = na, nb
  fft(a, inverse=False)
  fft(b, inverse=False)
  c = a * b
  ifft(c)
  c = np.rint(np.real(c)).astype(np.int64)[:n]
  return c


@nb.njit(
  (nb.i8[:], nb.i8[:]),
  cache=True,
)
def solve(
  a: np.ndarray,
  b: np.ndarray,
) -> typing.NoReturn:
  a = np.hstack((np.array([0]), a))
  b = np.hstack((np.array([0]), b))
  c = convolve(a, b)
  n = a.size
  for x in c[1:2 * n + 1]:
    print(x)


def main() -> typing.NoReturn:
  n = int(input())
  a, b = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(n, 2).T
  solve(a, b)


main()
