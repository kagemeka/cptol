import sys

n = int(sys.stdin.readline().rstrip())


def main():
    ans = (1 + n) * n // 2
    return ans


if __name__ == "__main__":
    ans = main()
    print(ans)
