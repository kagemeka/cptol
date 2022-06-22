import typing


class FindDivisors():
  def __call__(
    self,
    n: int,
  ) -> typing.List[int]:
    a = []
    i = 1
    while i * i < n:
      if n % i:
        i += 1
        continue
      a.append(i)
      a.append(n // i)
      i += 1
    if i * i == n: a.append(i)
    a.sort()
    return a



def euler_totient(
  n: int,
) -> int:
  c = m = n
  p = 2
  while p * p <= n:
    if m % p:
      p += 1
      continue
    c = c // p * (p - 1)
    while not m % p: m //= p
    p += 1
  if m > 1:
    c = c // m * (m - 1)
  return c



def main() -> typing.NoReturn:
  p = int(input())
  n = p - 1
  divs = FindDivisors()(n)
  mod = 998244353
  s = 1
  for d in divs:
    s += euler_totient(d) * d
    s %= mod
  print(s)


main()
