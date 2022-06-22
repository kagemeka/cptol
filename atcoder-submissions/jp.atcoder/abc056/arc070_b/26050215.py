import sys
import typing

import numpy as np


def solve(a: np.ndarray, k: int) -> typing.NoReturn:
    n = a.size
    np.minimum(a, k)
    a.sort()

    def compute_dp(a):
        dp = np.zeros((n + 1, k), np.int16)
        dp[0, 0] = 1
        for i in range(n):
            dp[i + 1] |= dp[i]
            dp[i + 1, a[i] :] |= dp[i, : -a[i]]
        return dp

    dp_l = compute_dp(a)
    dp_r = compute_dp(a[::-1])[::-1]
    np.cumsum(dp_r, axis=1, out=dp_r)

    def is_needed(i):
        l = dp_l[i]
        r = dp_r[i + 1]
        for x in range(k):
            if not l[x]:
                continue
            s = r[k - 1 - x]
            if k - a[i] - x > 0:
                s -= r[k - a[i] - x - 1]
            if s >= 1:
                return True
        return False

    def binary_search():
        lo, hi = -1, n
        while hi - lo > 1:
            i = (lo + hi) // 2
            if is_needed(i):
                hi = i
            else:
                lo = i
        return hi

    print(binary_search())


def main() -> typing.NoReturn:
    n, k = map(int, input().split())
    a = np.array(
        sys.stdin.readline().split(),
        dtype=np.int32,
    )
    solve(a, k)


main()
