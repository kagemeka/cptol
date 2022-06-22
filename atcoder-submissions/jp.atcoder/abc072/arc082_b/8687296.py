import sys


def main():
    n, *p = map(int, sys.stdin.read().split())
    p = [None] + p + [None]
    cnt = 0
    i = 1
    while i <= n:
        if p[i] == i:
            cnt += 1
            if p[i + 1] == i + 1:
                i += 1
        i += 1

    print(cnt)


if __name__ == "__main__":
    main()
