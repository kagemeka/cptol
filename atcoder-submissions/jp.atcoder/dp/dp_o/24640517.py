import sys
import typing

import numpy as np


def bit_count(
  n: int,
) -> np.array:
  a = np.zeros(n, np.int64)
  for i in range(n):
    a[i] = a[i // 2] + i % 2
  return a


def solve(
  n: int,
  a: np.array,
) -> typing.NoReturn:
  a = a.astype(np.bool8)
  mod = 10 ** 9 + 7
  dp = np.zeros(
    1 << n,
    dtype=np.int64,
  )
  dp[0] = 1
  bitcnt = bit_count(1 << 22)

  for s in range(1 << n):
    c = bitcnt[s]
    for i in range(n):
      if ~s >> i & 1: continue
      if a[c - 1][i] == 0:
        continue
      dp[s] += dp[s - (1 << i)]
    dp[s] %= mod

  print(dp[-1])



def main() -> typing.NoReturn:
  n = int(input())
  a = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  ).reshape(n, n)
  solve(n, a)



OJ = 'ONLINE_JUDGE'
if sys.argv[-1] == OJ:
  from numba import i8, njit
  from numba.pycc import CC
  cc = CC('my_module')
  fn = solve
  signature = (i8, i8[:, :])
  bit_count = njit(bit_count)
  cc.export(
    fn.__name__,
    signature,
  )(fn)
  cc.compile()
  exit(0)


from my_module import solve

main()
