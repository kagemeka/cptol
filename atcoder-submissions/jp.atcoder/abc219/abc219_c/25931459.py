import sys
import typing

import numba as nb
import numpy as np


def solve() -> typing.NoReturn:
  ...



def main() -> typing.NoReturn:
  x = input()
  n = int(input())
  s = sys.stdin.read().split()
  ord_ = dict()
  for i in range(26):
    ord_[x[i]] = i


  def convert(s: str):
    return tuple(ord_[x] for x in s)

  s.sort(key=lambda x: convert(x))
  print(*s, sep='\n')



main()
