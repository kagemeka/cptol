n, m, *ab = [int(x) for x in open(0).read().split()]

from_1, to_n = set(), set()
for a, b in zip(*[iter(ab)] * 2):
    if a == 1:
        from_1.add(b)
    elif b == n:
        to_n.add(a)
print("POSSIBLE" if from_1 and to_n else "IMPOSSIBLE")

# 大嘘。これで通ったら...
