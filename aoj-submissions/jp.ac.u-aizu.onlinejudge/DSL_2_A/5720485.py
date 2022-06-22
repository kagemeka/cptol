import typing
import sys



class SegmentTree():
  def __getitem__(
    self,
    i: int,
  ) -> int:
    return self.__a[i]


  def __init__(
    self,
    height: int,
  ) -> typing.NoReturn:
    n = 1 << height
    a = [0] * (n << 1)
    self.__n = n
    self.__a = a


  def __len__(self) -> int:
    return self.__n


  def __repr__(self) -> str:
    return str(self.__a)


  def __setitem__(
    self,
    i: int,
    x: int,
  ) -> typing.NoReturn:
    self.__a[i] = x



class RMQ():
  def __init__(
    self,
    height: int,
    inf: int,
  ) -> typing.NoReturn:
    seg = SegmentTree(height)
    self.__inf = inf
    self.__seg = seg
    n = len(seg)
    for i in range(n):
      self[i] = inf
    self.__sl, self.__sr = 0, n
    self.__i = 1



  def __setitem__(
    self,
    i: int,
    x: int,
  ) -> typing.NoReturn:
    seg = self.__seg
    i += len(seg)
    seg[i] = x; i >>= 1
    while i:
      seg[i] = min(
        seg[i << 1],
        seg[i << 1 | 1],
      )
      i >>= 1


  def min(
    self,
    l: int,
    r: int,
  ) -> int:
    sl = self.__sl
    sr = self.__sr
    i = self.__i
    if r <= sl or sr <= l:
      return self.__inf
    if l <= sl and sr <= r:
      return self.__seg[i]
    sc = (sl + sr) // 2
    self.__i = i << 1
    self.__sr = sc
    lmin = self.min(l, r)
    self.__i = i << 1 | 1
    self.__sl = sc
    self.__sr = sr
    rmin = self.min(l, r)
    self.__sl = sl
    self.__i = i
    return min(lmin, rmin)



def solve(
  q: typing.List[
    typing.Tuple[int],
  ],
) -> typing.NoReturn:
  inf = (1 << 31) - 1
  h = 17
  rmq = RMQ(h, inf)
  for com, x, y in q:
    if com == 0:
      rmq[x] = y
    else:
      print(rmq.min(
        x, y + 1,
      ))



def main() -> typing.NoReturn:
  n, q = map(
    int,
    input().split(),
  )
  q = [
    tuple(
      int(x)
      for x in (
        sys.stdin.readline()
        .split()
      )
    )
    for _ in range(q)
  ]
  solve(q)


main()
