import sys
import typing

import numpy as np


def solve(a: np.ndarray, k: int) -> typing.NoReturn:
    n = len(a)
    a = np.minimum(a, k, out=a)
    a.sort()

    def compute_dp(a: np.ndarray) -> np.ndarray:
        dp = np.zeros((n + 1, k), np.bool8)
        dp[0, 0] = True
        for i in range(n):
            dp[i + 1] |= dp[i]
            dp[i + 1, a[i] :] |= dp[i, : -a[i]]
        return dp

    dp_l = compute_dp(a)
    dp_r = compute_dp(a[::-1])[::-1].astype(np.int16)
    np.cumsum(dp_r, axis=1, out=dp_r)

    def is_needed(i: int) -> bool:
        r = dp_r[i + 1]
        r[a[i] :] -= r[: -a[i]]
        return np.any(dp_l[i, ::-1] * r)

    def binary_search() -> int:
        lo, hi = -1, n
        while hi - lo > 1:
            i = (lo + hi) >> 1
            if is_needed(i):
                hi = i
            else:
                lo = i
        return hi

    print(binary_search())


def main() -> typing.NoReturn:
    n, k = map(int, input().split())
    a = np.array(sys.stdin.readline().split(), dtype=np.int32)
    solve(a, k)


main()
