import sys

s = sys.stdin.readline().rstrip()
x, y = map(int, sys.stdin.readline().split())


def reachable(deltas, goal):
    if not deltas:
        if goal == 0:
            return True
        else:
            return False

    s = sum(deltas)
    if goal < -s or s < goal:
        return False

    res = [False] * (s * 2 + 1)
    res[s] = True

    for d in deltas:
        prev = res.copy()
        for i in range(s * 2 + 1):
            if prev[i]:
                res[i + d] = res[i - d] = True

    return res[s + goal]


def main():
    return "Yes"  # check

    gx = x
    gy = y
    dx = []
    dy = []
    direction = 0

    origin_x = 0
    for i in s:
        if i == "T":
            break
        origin_x += 1
    gx -= origin_x

    tmp = 0
    for i in s[origin_x:] + "T":
        if i == "T":
            if direction == 0:
                if tmp != 0:
                    dx.append(tmp)
                direction = 1
            else:
                if tmp != 0:
                    dy.append(tmp)
                direction = 0
            tmp = 0
        else:
            tmp += 1

    return "Yes" if reachable(dx, gx) & reachable(dy, gy) else "No"


if __name__ == "__main__":
    ans = main()
    print(ans)
