import sys
import typing


def main() -> typing.NoReturn:
    n = int(input())
    (*t,) = map(int, sys.stdin.read().split())
    print(min(t))


main()
