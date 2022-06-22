class Reader:
    @staticmethod
    def readline():
        import sys

        return sys.stdin.buffer.readline().rstrip()

    @classmethod
    def read_int(cls):
        i = int(cls.readline())
        return i

    @classmethod
    def read_str(cls):
        s = cls.readline().decode()
        return s

    @classmethod
    def readline_ints(cls):
        (*ints,) = map(
            int,
            cls.readline().split(),
        )
        return ints

    @classmethod
    def readline_strs(cls):
        s = cls.read_str().split()
        return s

    @staticmethod
    def read():
        import sys

        i = sys.stdin.buffer.read()
        return i

    @classmethod
    def read_ints(cls):
        (*ints,) = map(
            int,
            cls.read().split(),
        )
        return ints

    @classmethod
    def read_strs(cls):
        return cls.read().decode().split()

    @staticmethod
    def readlines():
        import sys

        lines = sys.stdin.buffer.readlines()
        lines = [l.rstrip() for l in lines]
        return lines


class ReaderNumpy(Reader):
    @classmethod
    def readline_ints(cls):
        import numpy as np

        return np.fromstring(
            string=cls.read_str(),
            dtype=np.int64,
            sep=" ",
        )

    @classmethod
    def read_ints(cls):
        import numpy as np

        return np.fromstring(
            string=cls.read().decode(),
            dtype=np.int64,
            sep=" ",
        )


class Modular:
    def __init__(self, n: int, mod: int = 10**9 + 7):
        self.value = n
        self.value %= mod
        self.mod = mod

    def __repr__(self) -> str:
        return f"{self.value}"

    def clone(self):
        return self.__class__(self.value, self.mod)

    def modularize(self, other):
        if type(other) == int:
            other = self.__class__(
                other,
                self.mod,
            )
        return other

    def __iadd__(self, other):
        other = self.modularize(
            other,
        )
        self.value += other.value
        self.value %= self.mod
        return self

    def __add__(self, other):
        res = self.clone()
        res += other
        return res

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return self.modularize(
            -self.value,
        )

    def __sub__(self, other):
        res = self.clone()
        res += -other
        return res

    def __rsub__(self, other):
        other = self.modularize(
            other,
        )
        return other - self

    def __imul__(self, other):
        other = self.modularize(
            other,
        )
        self.value *= other.value
        self.value %= self.mod
        return self

    def __mul__(self, other):
        res = self.clone()
        res *= other
        return res

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = self.modularize(
            other,
        )
        res = self.clone()
        res *= other.invert()
        return res

    def __rtruediv__(self, other):
        other = self.modularize(
            other,
        )
        return other / self

    def __floordiv__(self, other):
        return self / other

    def __rfloordiv__(self, other):
        return other / self

    def pow(self, n):
        if n == 0:
            return self.modularize(
                1,
            )
        a = self.pow(n >> 1)
        a *= a
        if n & 1:
            a *= self
        return a

    def __ipow__(self, other):
        other = self.modularize(
            other,
        )

        self.value = pow(
            self.value,
            other.value,
            self.mod,
        )
        return self

    def __pow__(self, other):
        res = self.clone()
        res **= other
        return res

    def __rpow__(self, other):
        other = self.modularize(
            other,
        )
        return other**self

    def invert(self):
        return self ** (self.mod - 2)


Mint = Modular


class Solver:
    def __init__(self):
        self.reader = Reader()
        # self.reader = ReaderNumpy()
        self.mod = 10**9 + 7

    def __prepare(self):
        reader = self.reader
        a, b, c = reader.read_ints()
        mod = self.mod
        self.a = Mint(a, mod)
        self.b = Mint(b, mod)
        self.c = Mint(c, mod)

    def __solve(self):
        a = self.a
        b = self.b
        c = self.c
        denom = a * b - b * c + c * a
        denom = denom.invert()
        w = (b * c - a * b) * denom
        h = (b * c - a * c) * denom
        print(h, w)

    def run(self):
        self.__prepare()
        self.__solve()


def main():
    t = 1
    # t = Reader.read_int()
    for _ in range(t):
        solver = Solver()
        solver.run()


if __name__ == "__main__":
    main()
