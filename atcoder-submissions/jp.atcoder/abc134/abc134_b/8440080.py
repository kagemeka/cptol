# 2019-11-15 14:12:24(JST)
# import collections
import math
import sys

# from string import ascii_lowercase, ascii_uppercase, digits
# from bisect import bisect_left as bi_l, bisect_right as bi_r
# import itertools
# from functools import reduce
# import operator as op
# from scipy.misc import comb # float
# import numpy as np

def main():
    n, d = [int(x) for x in sys.stdin.readline().split()]
    ran = 1 + d * 2
    number = math.ceil(n / ran)
    print(number)

if __name__ == "__main__":
    main()
