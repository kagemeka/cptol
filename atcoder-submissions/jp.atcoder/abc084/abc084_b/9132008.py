import sys

a, b = map(int, sys.stdin.readline().split())
s = sys.stdin.readline().rstrip()


def main():
    return (
        "Yes" if s[a] == "-" and not "-" in set(s[:a] + s[a + 1 :]) else "No"
    )


if __name__ == "__main__":
    ans = main()
    print(ans)
