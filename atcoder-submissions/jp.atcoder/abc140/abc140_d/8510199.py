# 2019-11-18 00:38:19(JST)
# import collections
# import math
# from string import ascii_lowercase, ascii_uppercase, digits
# from bisect import bisect_left as bi_l, bisect_right as bi_r
# import itertools
# from functools import reduce
# import operator as op
import re
import sys

# import heapq
# import array
# from scipy.misc import comb # (default: exact=False)
# import numpy as np


def main():
    n, k = [int(x) for x in sys.stdin.readline().split()]
    s = sys.stdin.readline().rstrip()

    # R を反転させる
    unhappy_count = 0
    if s[0] == 'L':
        unhappy_count += 1
    if s[-1] == 'R':
        unhappy_count += 1

    two_unhappy = [c.start() for c in re.finditer('RL', s)]

    if k <= len(two_unhappy):
        unhappy_count += 2 * (len(two_unhappy) - k)
    else:
        unhappy_count = max(0, unhappy_count - (k - len(two_unhappy)))

    happy_count = n - unhappy_count

    print(happy_count)



if __name__ == "__main__":
    main()
