import sys
import typing

import numba as nb
import numpy as np


@nb.njit((nb.i8[:], ), cache=True)
def solve(a: np.ndarray) -> typing.NoReturn:
    n = len(a)
    prev = np.empty(n, np.int64)
    last = np.zeros(26, np.int64)
    for i in range(n):
        prev[i] = last[a[i]]
        last[a[i]] = i + 1
    mod = 10 ** 9 + 7

    dp = np.zeros(n + 2, np.int64)
    for i in range(2, n + 2):
        j = prev[i - 2]
        dp[i] = dp[i - 2] - dp[j] + (j == 0)
        dp[i] = (dp[i] + dp[i - 1]) % mod
    print(dp[-1])


def main() -> typing.NoReturn:
    a = np.array([ord(x) - 97 for x in input()])
    solve(a)


main()
