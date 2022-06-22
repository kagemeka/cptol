import math
import sys


def main():
    a, b, k = map(int, sys.stdin.readline().split())
    query_range = list(range(a, b + 1))

    if a == b:
        res = query_range
    elif k >= math.ceil((b - a + 1) / 2):
        res = query_range
    else:
        res = query_range[:k] + query_range[-k:]

    for i in res:
        print(i)


if __name__ == "__main__":
    main()
