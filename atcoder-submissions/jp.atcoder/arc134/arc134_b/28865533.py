import heapq
import typing


def main() -> None:
    n = int(input())
    s = list(input())
    hq = []
    for i, c in enumerate(s):
        heapq.heappush(hq, (c, -i))

    mn_right = n
    for i in range(n):
        if i >= mn_right:
            break
        while hq:
            c, j = heapq.heappop(hq)
            j *= -1
            if i < j < mn_right:
                break

        else:
            continue
        if c >= s[i]:
            heapq.heappush(hq, (c, -j))
            continue
        assert i < j < mn_right
        s[i], s[j] = s[j], s[i]
        mn_right = j
    print("".join(s))


if __name__ == "__main__":
    main()
