import sys
from bisect import bisect_left as bi_l
from math import ceil

n, d, a, *xh = map(int, sys.stdin.read().split())
xh = [(x, ceil(h / a)) for x, h in sorted(zip(*[iter(xh)] * 2))]

def main():
    cnt = 0
    l = 0
    r = []
    s = []
    tmp = 0
    i = 0
    while l < n:
        x, h = xh[l]
        if bi_l(r, x) > i:
            tmp -= s[i]
            i += 1
        if h - tmp <= 0:
            l += 1
            continue
        cnt += h - tmp
        r.append(x + d * 2)
        s.append(h - tmp)
        tmp += h - tmp
        l += 1
    return cnt

if __name__ == '__main__':
    ans = main()
    print(ans)
