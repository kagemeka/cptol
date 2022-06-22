import sys
import typing

import numpy as np

# import numba as nb



# @nb.njit
def fw_add(
  a: np.array,
  i: int,
  x: int,
) -> typing.NoReturn:
  while i < a.size:
    a[i] += x
    i += i & -i



# @nb.njit
def fw_sum(
  a: np.array,
  i: int,
) -> int:
  s = 0
  while i > 0:
    s += a[i]
    i -= i & -i
  return s


# @nb.njit(
#   (nb.i8, nb.i8[:], nb.i8[:]),
#   cache=True,
# )
def solve(
  n: int,
  a: np.array,
  q: np.array,
) -> typing.NoReturn:
  fw = np.zeros(
    n + 1,
    dtype=np.int64,
  )
  for i in range(n):
    fw_add(fw, i + 1, a[i])
  n = q.size // 3
  for i in range(n):
    t, x, y = q[
      i * 3:(i + 1) * 3
    ]
    if t == 0:
      fw_add(fw, x + 1, y)
      continue
    s = fw_sum(fw, y)
    s -= fw_sum(fw, x)
    print(s)



def main() -> typing.NoReturn:
  n, q = map(
    int, input().split(),
  )
  a = np.array(
    sys.stdin.readline()
    .split(),
    dtype=np.int64,
  )
  q = np.array(
    sys.stdin.read().split(),
    dtype=np.int64,
  )
  solve(n, a, q)


if (
  sys.argv[-1]
  == 'ONLINE_JUDGE'
):
  from numba import i8, njit

  fw_add = njit(fw_add)
  fw_sum = njit(fw_sum)

  fn = solve
  signature = (
    i8,
    i8[:],
    i8[:],
  )

  from numba.pycc import CC
  cc = CC('my_module')
  cc.export(
    fn.__name__,
    signature,
  )(fn)
  cc.compile()
  exit(0)


from my_module import solve

main()
