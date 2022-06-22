import sys

cand = set()
for i in range(0, 100 + 1, 4):
    for j in range(0, 100 - i + 1, 7):
        cand.add(i + j)

n = int(sys.stdin.readline().rstrip())


def main():
    return "Yes" if n in cand else "No"


if __name__ == "__main__":
    ans = main()
    print(ans)
