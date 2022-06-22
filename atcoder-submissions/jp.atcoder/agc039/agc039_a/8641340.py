# 2019-11-25 06:26:24(JST)
import sys


def main():
    s, k = sys.stdin.read().split()
    k = int(k)

    count = 0
    same = 1
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            same += 1
        else:
            if count == 0:
                first_same = same
            count += same // 2
            same = 1

    bl = False
    if s[-1] == s[0]:
        if same % 2 == 1 and first_same % 2 == 1:
            count += same // 2 + 1
            bl = True
        else:
            count += same // 2
    else:
        count += same // 2

    ans = count * k
    if bl:
        ans -= 1

    print(ans)

if __name__ == '__main__':
    main()
