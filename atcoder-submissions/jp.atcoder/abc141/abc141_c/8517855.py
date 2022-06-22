# 2019-11-18 17:34:23(JST)
import collections
import sys

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
    n, k, q, *a = [int(x) for x in sys.stdin.read().split()]

    c = collections.Counter(a)
    for i in range(1, n+1):
        if not i in c:
            print('No' if k - q <= 0 else 'Yes')
        else:
            print('No' if k - (q - c[i]) <= 0 else 'Yes')


if __name__ == "__main__":
    main()
