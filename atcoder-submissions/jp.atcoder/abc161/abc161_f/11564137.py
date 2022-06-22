import sys
from math import floor, sqrt


def divisors(n):
    res = set()
    for i in range(1, floor(sqrt(n)) + 1):
        if not n % i:
            res.add(i)
            res.add(n // i)
    return res - set([1])

n = int(sys.stdin.readline().rstrip())

def main():
    res = divisors(n - 1)
    cnt = len(res)
    for i in divisors(n):
        m = n
        while not m % i:
            m //= i
        if (m - 1) % i == 0:
            cnt += 1
    print(cnt)

if __name__ ==  '__main__':
    main()
