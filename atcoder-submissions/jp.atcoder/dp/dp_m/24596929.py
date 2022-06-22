import sys
import typing

import numpy as np


def solve(
  k: int,
  a: np.array,
) -> typing.NoReturn:
  mod = 10 ** 9 + 7
  dp = np.zeros(
    k + 1,
    dtype=np.int64,
  )
  dp[0] = 1
  for x in a:
    x += 1
    dp[x:] -= dp.copy()[:-x]
    dp = np.cumsum(dp)
    dp %= mod
  print(dp[-1])


def main() -> typing.NoReturn:
  n, k = map(
    int, input().split(),
  )
  a = np.array(
    sys.stdin.readline()
    .split(),
    dtype=np.int64,
  )
  solve(k, a)


OJ = 'ONLINE_JUDGE'
if sys.argv[-1] == OJ:
  from numba import i8
  from numba.pycc import CC

  cc = CC('my_module')
  fn = solve
  signature = (i8, i8[:])

  cc.export(
    fn.__name__,
    signature,
  )(fn)
  cc.compile()
  exit(0)


from my_module import solve

main()
