import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:], nb.i8), cache=True)
def mod_cumprod(a: np.ndarray, mod: int) -> typing.NoReturn:
  for i in range(a.size - 1): a[i + 1] = a[i + 1] * a[i] % mod


@nb.njit((nb.i8, nb.i8), cache=True)
def mod_factorial(n: int, mod: int) -> np.ndarray:
  a = np.arange(n)
  a[0] = 1
  mod_cumprod(a, mod)
  return a


@nb.njit((nb.i8, nb.i8, nb.i8), cache=True)
def mod_pow(x: int, n: int, mod: int) -> int:
  y = 1
  while n:
    if n & 1: y = y * x % mod
    x = x * x % mod
    n >>= 1
  return y


@nb.njit((nb.i8, nb.i8), cache=True)
def mod_inverse(a: int, p: int) -> int:
  return mod_pow(a, p - 2, p)



@nb.njit((nb.i8, nb.i8), cache=True)
def mod_inverse_factorial(n: int, mod: int) -> np.ndarray:
  a = np.arange(1, n + 1)
  a[-1] = mod_inverse(mod_factorial(n, mod)[-1], mod)
  mod_cumprod(a[::-1], mod)
  return a


@nb.njit
def solve(n: int, k: int) -> typing.NoReturn:
  mod = 10 ** 9 + 7
  m = 1 << 20
  fact = mod_factorial(m, mod)
  ifact = mod_inverse_factorial(m, mod)

  def nCk(n, k):
    nonlocal fact, ifact, mod
    ok = (0 <= k) & (k <= n)
    return fact[n] * ifact[k] % mod * ifact[n - k] % mod * ok

  def nHk(n, k):
    return nCk(n + k - 1, k)


  cnt = nHk(n, n)
  if k >= n - 1:
    print(cnt)
    return

  for i in range(k + 1, n + 1):
    cnt -= nCk(n, i) * nHk(n - i, i) % mod
  print(cnt % mod)



def main():
  n, k = map(int, input().split())
  solve(n, k)


main()
