# 2019-11-23 21:00:35(JST)
import collections
import sys


def main():
    m = int(sys.stdin.readline().rstrip())

    a = collections.defaultdict(int)
    for _ in range(m):
        d, c = map(int, sys.stdin.readline().split())
        a[d] += c


    b = 0
    for i in range(10):
        b += (i + 9) * a[i]

    ans = b // 9 - 1
    print(ans)



if __name__ == '__main__':
    main()
