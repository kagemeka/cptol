from collections import Counter


def main():
  n, k = map(
    int,
    input().split(),
  )
  *c, = map(
    int,
    input().split(),
  )
  cnt = Counter(c[:k])
  mx = len(cnt)
  for i in range(k, n):
    x = c[i - k]
    cnt[x] -= 1
    if cnt[x] == 0:
      cnt.pop(x)
    cnt[c[i]] += 1
    mx = max(mx, len(cnt))
  print(mx)



main()
