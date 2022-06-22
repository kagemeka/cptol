# 2019-11-14 17:27:23(JST)
import itertools
import sys

# import collections
# import math
# from string import ascii_lowercase, ascii_uppercase, digits
from bisect import bisect_left as bi_l
from bisect import bisect_right as bi_r

# from functools import reduce
# import operator as op
# from scipy.misc import comb # float
# import numpy as np

def main():
    n, k, *A = [int(x) for x in sys.stdin.read().split()]

    total = 0
    s = list(itertools.accumulate(A))
    index = bi_l(s, k)
    count = n - index
    total += count
    for i in range(n):
        if index == n:
            break
        for j in range(index, n):
            s[j] -= A[i]
        if s[index] >= k:
            total += count
        else:
            index = bi_l(s, k)
            count = n - index
            total += count

    print(total)


if __name__ == "__main__":
    main()
