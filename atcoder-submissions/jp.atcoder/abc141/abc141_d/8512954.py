# 2019-11-18 17:34:23(JST)
import sys

# import collections
# import math
# from string import ascii_lowercase, ascii_uppercase, digits
# from bisect import bisect_left as bi_l, bisect_right as bi_r
# import itertools
# from functools import reduce
# import operator as op
# import re
# import heapq
# import array
# from scipy.misc import comb # (default: exact=False)
# import numpy as np


def main():
    n, m, *a = [int(x) for x in sys.stdin.read().split()]

    for _ in range(m):
        a.sort()
        a[-1] //= 2

    print(sum(a))



if __name__ == "__main__":
    main()
