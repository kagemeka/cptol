import sys
from string import digits


def main():
    n, s = sys.stdin.read().split()
    n = int(n)

    place = dict((i, set()) for i in digits)
    for i in range(n):
        place[s[i]].add(i)

    l = [None] * n
    l[0] = set()
    for i in range(1, n):
        l[i] = l[i-1] | set([s[i-1]])

    r = [None] * n
    r[n-1] = set()
    for i in range(n-2, -1, -1):
        r[i] = r[i+1] | set([s[i+1]])

    res = set()
    for j in digits:
        for c in place[j]:
            for i in digits:
                if i in l[c]:
                    for k in digits:
                        if k in r[c]:
                            res.add((i, j, k))

    print(len(res))


if __name__ == '__main__':
    main()
