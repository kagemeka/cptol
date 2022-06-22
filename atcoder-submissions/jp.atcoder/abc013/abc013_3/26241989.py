import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8,) * 7, cache=True)
def solve(
    n: int,
    h: int,
    a: int,
    b: int,
    c: int,
    d: int,
    e: int,
) -> typing.NoReturn:
    mn = c * n
    for x in range(n + 1):
        y = (n * e - h - (b + e) * x) // (d + e) + 1
        y = max(y, 0)
        if not x + y <= n:
            continue
        mn = min(mn, a * x + c * y)
    print(mn)


def main() -> typing.NoReturn:
    n, h = map(int, input().split())
    a, b, c, d, e = map(int, input().split())
    solve(n, h, a, b, c, d, e)


main()
