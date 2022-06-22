import sys
from bisect import bisect_left as bi_l
from bisect import bisect_right as bi_r
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import product

import numpy as np

inf = float("inf")
MOD = 10**9 + 7
# MOD = 998244353


class ABC001:
    def A():
        h1, h2 = map(int, sys.stdin.read().split())
        print(h1 - h2)

    def B():
        pass

    def C():
        pass

    def D():
        pass


class ABC002:
    def A():
        x, y = map(int, sys.stdin.readline().split())
        print(max(x, y))

    def B():
        vowels = set("aeiou")
        s = sys.stdin.readline().rstrip()
        t = ""
        for c in s:
            if c in vowels:
                continue
            t += c
        print(t)

    def C():
        pass

    def D():
        pass


if __name__ == "__main__":
    ABC002.B()
