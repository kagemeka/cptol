import sys

import numpy as np

MOD = 10 ** 9 + 7

n, *a = map(int, sys.stdin.read().split())
a = np.array(a, dtype=np.int64)

def main():
    b = a >> np.arange(61).reshape(-1, 1) & 1
    x = np.count_nonzero(b, axis=1)
    x = x * (n - x) % MOD
    # x *= 2 ** np.arange(60) % MOD
    for i in range(1, 61):
        x[i] *= pow(2, i, MOD)
    x %= MOD
    ans = np.sum(x) % MOD
    return ans

if __name__ == '__main__':
    ans = main()
    print(ans)
