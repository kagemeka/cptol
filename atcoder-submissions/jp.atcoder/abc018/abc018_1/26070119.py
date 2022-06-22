import sys
import typing

import numpy as np


def main() -> typing.NoReturn:
    a = np.array(
        sys.stdin.read().split(),
        dtype=np.int64,
    )
    rank = np.argsort(np.argsort(a)[::-1]) + 1
    rank = rank.tolist()
    print(*rank, sep="\n")


main()
