import typing

import numba as nb
import numpy as np


@nb.njit
def find_divisors(
  n: int,
) -> np.array:
  i = np.arange(int(n ** .5))
  i += 1
  i = i[n % i == 0]
  i = np.hstack((i, n // i))
  return np.unique(i)



@nb.njit
def lpf(
  n: int = 1 << 20,
) -> np.array:
  s = np.arange(n)
  s[:2] = -1
  i = 0
  while i * i < n - 1:
    i += 1
    if s[i] == i: s[i::i] = i
  return s


@nb.njit
def spf(
  n: int = 1 << 20,
) -> np.array:
  s = np.arange(n)
  s[:2] = -1
  i = 0
  while i * i < n - 1:
    i += 1
    j = np.arange(i, n, i)
    # s[j][s[j] == j] = i
    for j in range(i, n, i):
      if s[j] == j: s[j] = i
  return s


@nb.njit
def sieve_of_eratosthenes(
  n: int = 1 << 20,
) -> np.array:
  return spf(n) == np.arange(n)



@nb.njit
def prime_numbers(
  n: int = 1 << 20,
) -> np.array:
  s = sieve_of_eratosthenes(n)
  return np.flatnonzero(s)



@nb.njit
def euler_totient(
  n: int,
  prime_numbers: np.array,
) -> int:
  c = n
  for p in prime_numbers:
    if p * p > n: break
    if n % p: continue
    c = c // p * (p - 1)
    while not n % p: n //= p
  if n > 1:
    c = c // n * (n - 1)
  return c


@nb.njit(
  (nb.i8, ),
  cache=True,
)
def solve(
  p: int,
) -> typing.NoReturn:
  n = p - 1
  divs = find_divisors(n)
  pn = prime_numbers(1 << 20)
  mod = 998244353
  c = 1
  for d in divs:
    e = euler_totient(d, pn)
    e %= mod
    d %= mod
    c += e * d % mod
    c %= mod
  print(c)


def main() -> typing.NoReturn:
  p = int(input())
  solve(p)


main()
