import sys
import typing

import numba as nb
import numpy as np


def solve() -> typing.NoReturn:
  ...



def main() -> typing.NoReturn:
  s1 = input()
  s2 = input()
  s3 = input()
  *t, = map(int, list(input()))
  n = len(t)
  a = [
    s1 if x == 1 else
    s2 if x == 2 else
    s3
    for x in t
  ]
  print(''.join(a))

main()
