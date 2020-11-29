if __name__ == "__main__":
    n, m = map(int, input().split())
    a = {i: set() for i in range(n)}
    for i in range(m):
        u, v, w = map(int, input().split())
        a[u].add((v, w))
        a[v].add((u, w))
    d = [(-1, -1, float("inf"))] * n
    for v, w in a[0]:
        d[v] = (0, v, w)
    T = {i for i in range(1, n)}
    edges = []
    weight = 0
    for _ in range(n - 1):
        j = -1
        min_w = float("inf")
        for v in T:
            if d[v][2] < min_w:
                min_w = d[v][2]
                j = v
        edges.append(d[j])
        weight += min_w
        T.remove(j)
        for v, w in a[j]:
            if w < d[v][2]:
                d[v] = (j, v, w)
    print(weight)
    print(*edges, sep="\n")
