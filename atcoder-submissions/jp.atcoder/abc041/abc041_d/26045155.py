import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8, nb.i8[:, :]), cache=True)
def solve(n: int, xy: np.ndarray) -> typing.NoReturn:
    m = len(xy)
    after = np.zeros(n, np.int64)
    for i in range(m):
        x, y = xy[i]
        after[x] |= 1 << y

    dp = np.zeros(1 << n, np.int64)
    dp[0] = 1

    for s in range(1 << n):
        for i in range(n):
            if ~s >> i & 1:
                continue
            u = s & ~(1 << i)
            dp[s] += 0 if u & after[i] else dp[u]
    print(dp[-1])


def main() -> typing.NoReturn:
    n, m = map(int, input().split())
    xy = (
        np.array(
            sys.stdin.read().split(),
            dtype=np.int64,
        ).reshape(m, 2)
        - 1
    )
    solve(n, xy)


main()
