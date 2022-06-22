import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:],), cache=True)
def solve(a: np.ndarray) -> typing.NoReturn:
    n = len(a)
    b = np.zeros(1 << 20, np.bool8)
    for i in range(n):
        while a[i] % 2 == 0:
            a[i] //= 2
        b[a[i]] = True
    print(np.count_nonzero(b))


def main() -> typing.NoReturn:
    n = int(input())
    a = np.array(
        sys.stdin.readline().split(),
        dtype=np.int64,
    )
    solve(a)


main()
