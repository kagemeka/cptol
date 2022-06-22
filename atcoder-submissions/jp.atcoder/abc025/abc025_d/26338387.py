import sys
import typing

import numba as nb
import numpy as np

# @nb.njit
# def bit_count(n: int) -> int:
#   cnt = 0
#   while n:
#     cnt += n & 1
#     n >>= 1
#   return cnt


@nb.njit
def bit_count_table(n) -> int:
    cnt = np.zeros(n, np.uint8)
    for i in range(1, n):
        cnt[i] = cnt[i >> 1] + (i & 1)
    return cnt


@nb.njit((nb.i1[:],), cache=True)
def solve(a: np.ndarray) -> typing.NoReturn:
    n = len(a)
    fixed_idx = np.full(n, -1, np.int8)
    fixed_val = np.full(n, -1, np.int8)
    is_fixed = 0
    for i in range(n):
        if a[i] == -1:
            continue
        fixed_idx[a[i]] = i
        fixed_val[i] = a[i]
        is_fixed |= 1 << a[i]

    cum_fixed_idx_set = np.zeros(n, np.uint32)
    for i in range(n):
        if not fixed_idx[i]:
            continue
        cum_fixed_idx_set[i] = 1 << fixed_idx[i]
    for i in range(n - 1):
        cum_fixed_idx_set[i + 1] |= cum_fixed_idx_set[i]

    bit_cnt = bit_count_table(1 << n)

    def can_transit(s, i):
        y, x = divmod(i, 5)
        if 1 <= y < 4 and (s >> i - 5 & 1) ^ (s >> i + 5 & 1):
            return False
        if 1 <= x < 4 and (s >> i - 1 & 1) ^ (s >> i + 1 & 1):
            return False
        return True

    def is_impossible(s):
        v = bit_cnt[s] - 1
        return s | cum_fixed_idx_set[v] != s

    mod = 1_000_000_007
    dp = np.empty(1 << n, np.uint32)
    dp[0] = 1
    s = 1
    while s <= 1 << n:
        # for s in range(1, 1 << n):
        if is_impossible(s):
            s += 1
            continue
        dp[s] = 0
        v = bit_cnt[s] - 1
        i = 0
        while i < n:
            # for i in range(n):
            if ~s >> i & 1:
                i += 1
                continue
            u = s & ~(1 << i)
            if fixed_idx[v] != -1 and fixed_idx[v] != i:
                i += 1
                continue
            if fixed_val[i] != -1 and fixed_val[i] != v:
                i += 1
                continue
            if not can_transit(u, i):
                i += 1
                continue
            dp[s] = (dp[s] + dp[u]) % mod
            i += 1
        s += 1
    print(dp[-1])


def main() -> typing.NoReturn:
    a = (
        np.array(
            sys.stdin.read().split(),
            dtype=np.int8,
        )
        - 1
    )
    solve(a)


main()
