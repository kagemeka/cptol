import sys
import typing
from collections import Counter
from functools import lru_cache

sys.setrecursionlimit(1 << 25)



def solve(
  n: int,
  a: typing.List[int],
) -> typing.NoReturn:
  @lru_cache(maxsize=None)
  def dfs(
    i: int,
    j: int,
    k: int,
  ) -> typing.NoReturn:
    nonlocal n
    s = i + j + k
    if s == 0: return 0
    e = n
    if i > 0:
      e += i * dfs(
        i - 1,
        j + 1,
        k,
      )
    if j > 0:
      e += j * dfs(
        i,
        j - 1,
        k + 1,
      )
    if k > 0:
      e += k * dfs(
        i,
        j,
        k - 1,
      )
    e /= s
    return e

  c = Counter(a)
  print(dfs(c[3], c[2], c[1]))


def main() -> typing.NoReturn:
  n = int(input())
  *a, = map(
    int, input().split(),
  )
  solve(n, a)


main()
