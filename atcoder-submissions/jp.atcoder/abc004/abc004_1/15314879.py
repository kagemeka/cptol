import sys
from bisect import bisect_left as bi_l
from bisect import bisect_right as bi_r
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from itertools import combinations, product

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
        (*coords,) = map(int, sys.stdin.readline().split())

        def triangle_area(x0, y0, x1, y1, x2, y2):
            x1 -= x0
            x2 -= x0
            y1 -= y0
            y2 -= y0
            return abs(x1 * y2 - x2 * y1) / 2

        print(triangle_area(*coords))

    def D():
        n, m = map(int, sys.stdin.readline().split())
        edges = set()
        for _ in range(m):
            x, y = map(int, sys.stdin.readline().split())
            x -= 1
            y -= 1
            edges.add((x, y))
        cand = []
        for i in range(1, 1 << n):
            s = [j for j in range(n) if i >> j & 1]
            for x, y in combinations(s, 2):
                if (x, y) not in edges:
                    break
            else:
                cand.append(len(s))
        print(max(cand))


class ABC003:
    def A():
        n = int(sys.stdin.readline().rstrip())
        print((n + 1) * 5000)

    def B():
        atcoder = set("atcoder")
        s, t = sys.stdin.read().split()
        for i in range(len(s)):
            if s[i] == t[i]:
                continue
            if s[i] == "@" and t[i] in atcoder:
                continue
            if t[i] == "@" and s[i] in atcoder:
                continue
            print("You will lose")
            return
        print("You can win")

    def C():
        n, k, *r = map(int, sys.stdin.read().split())
        res = 0
        for x in sorted(r)[-k:]:
            res = (res + x) / 2
        print(res)

    def D():
        pass


class ABC004:
    def A():
        print(int(sys.stdin.readline().rstrip()) * 2)

    def B():
        c = [sys.stdin.readline().rstrip() for _ in range(4)]
        for l in c[::-1]:
            print(l[::-1])

    def C():
        n = int(sys.stdin.readline().rstrip())
        n %= 30
        res = list(range(1, 7))
        for i in range(n):
            i %= 5
            res[i], res[i + 1] = res[i + 1], res[i]
        print("".join(map(str, res)))

    def D():
        pass


if __name__ == "__main__":
    ABC004.A()
