# 2019-11-22 19:46:21(JST)
import sys


def main():
    n, a, b, c, d = [int(x) for x in sys.stdin.readline().split()]
    s = '#' + sys.stdin.readline().rstrip()

    if '##' in s[a+1:c-1] or '##' in s[b+1:d-1]:
        ans = 'No'
    else:
        if c < d:
            ans = 'Yes'
        else:
            if '...' in s[b-1:d]:
                ans = 'Yes'
            else:
                ans = 'Yes'

    print(ans)

if __name__ == '__main__':
    main()
