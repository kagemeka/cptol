import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

n = int(sys.stdin.readline().rstrip())
xy = np.array(sys.stdin.read().split(), dtype=np.int64).reshape(-1, 2).T


def main():
    indices1, indices2 = np.argsort(xy)
    res1 = xy[:, indices1]
    res2 = xy[:, indices2]
    d1 = np.absolute(res1[:, 1:] - res1[:, :-1])
    d1 = np.amin(d1, axis=0)
    d2 = np.absolute(res2[:, 1:] - res2[:, :-1])
    d2 = np.amin(d2, axis=0)
    d = np.concatenate((d1, d2))

    a = np.concatenate((indices1[:-1], indices2[:-1]))
    b = np.concatenate((indices1[1:], indices2[1:]))

    graph = coo_matrix((d, (a, b)), shape=(n, n)).tocsr()
    res = minimum_spanning_tree(graph, overwrite=True)
    return int(np.sum(res))


if __name__ == "__main__":
    ans = main()
    print(ans)
