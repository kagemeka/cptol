import sys
import typing


def main() -> typing.NoReturn:
    n = int(input())
    n += n >= 42
    print(f'AGC{n:03}')

main()
