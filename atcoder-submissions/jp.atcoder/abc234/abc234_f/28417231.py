import collections
import typing


def cumprod(mod: int, a: typing.List[int]) -> typing.List[int]:
    """Compute cummulative product over Modular."""
    a = a.copy()
    for i in range(len(a) - 1):
        a[i + 1] = a[i + 1] * a[i] % mod
    return a


def factorial(mod: int, n: int) -> typing.List[int]:
    fact = list(range(n))
    fact[0] = 1
    return cumprod(mod, fact)


def factorial_inverse(p: int, n: int) -> typing.List[int]:
    ifact = list(range(1, n + 1))
    ifact[-1] = pow(factorial(p, n)[-1], p - 2, p)
    return cumprod(p, ifact[::-1])[::-1]


def make_choose(
    mod: int,
    n: int,
) -> typing.Callable[[int, int], int]:
    fact = factorial(mod, n)
    ifact = factorial_inverse(mod, n)

    def choose(n: int, k: int) -> int:
        nonlocal fact, ifact
        if k < 0 or n < k:
            return 0
        return fact[n] * ifact[n - k] % mod * ifact[k] % mod

    return choose



def main() -> None:
    s = input()
    # len(s) <= 5000
    MOD = 998_244_353

    # regardless of indices
    # it depends only on the kinds of letters.

    # 1. DP
    # 2. comppute answer for each length.

    n = len(s)

    choose = make_choose(MOD, 1 << 13)

    dp = [0] * (n + 1)
    dp[0] = 1
    cnt = collections.Counter(s)

    for c in cnt.values():
        for i in range(n, 0, -1):
            for j in range(1, c + 1):
                if i - j < 0: break
                dp[i] += dp[i - j] * choose(i, j) % MOD
                dp[i] %= MOD

    print((sum(dp) - 1) % MOD)




main()
