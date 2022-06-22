import sys
import typing

import numpy as np


def main():
  n = int(input())
  a = np.array(
    sys.stdin.readline()
    .split(),
    dtype=np.int64,
  )
  i = np.argsort(a)
  print(i[-2] + 1)


main()
