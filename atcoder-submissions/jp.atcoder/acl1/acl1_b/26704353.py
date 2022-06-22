

import typing

import numba as nb
import numpy as np


@nb.njit
def extgcd(a: int, b: int) -> typing.Tuple[int, int, int]:
    if not b: return a, 1, 0
    g, s, t = extgcd(b, a % b)
    return g, t, s - a // b * t


@nb.njit
def crt(r: np.ndarray, m: np.ndarray) -> typing.Tuple[int, int]:
    r0, m0 = 0, 1
    assert r.size == m.size
    for i in range(r.size):
        r1, m1 = r[i], m[i]
        d, p, q = extgcd(m0, m1)
        if (r1 - r0) % d: return 0, 0
        u1 = m1 // d
        r0 += (r1 - r0) // d % u1 * p % u1 * m0
        m0 *= u1
        r0 %= m0
    return r0, m0


@nb.njit
def find_divisors(n: int) -> np.ndarray:
    i = np.arange(int(n ** .5)) + 1
    i = i[n % i == 0]
    return np.unique(np.hstack((i, n // i)))



@nb.njit((nb.i8, ), cache=True)
def solve(n: int) -> typing.NoReturn:
    divs = find_divisors(2 * n)
    k = 1 << 30
    for d in divs:
        rs = np.array([0, -1])
        ms = np.array([d, 2 * n // d])
        r, l = crt(rs, ms)
        assert l >= r >= 0
        if l == 0 or r == 0: continue
        k = min(k, r)
    print(k)



def main() -> typing.NoReturn:
    n = int(input())
    solve(n)

main()
