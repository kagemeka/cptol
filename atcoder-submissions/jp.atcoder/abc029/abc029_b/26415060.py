import sys
import typing


def main() -> typing.NoReturn:
    s = sys.stdin.read().split()
    print(sum("r" in x for x in s))


main()
