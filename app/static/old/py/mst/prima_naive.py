if __name__ == "__main__":
    n, m = map(int, input().split())
    a = {i: set() for i in range(n)}
    for i in range(m):
        u, v, w = map(int, input().split())
        a[u].add((v, w))
        a[v].add((u, w))
    S = {0}
    edges = []
    weight = 0
    for _ in range(n - 1):
        u = -1
        j = -1
        min_w = float("inf")
        for u in S:
            for v, w in a[u]:
                if v not in S and w < min_w:
                    min_w = w
                    i = u
                    j = v
        edges.append((i, j, min_w))
        weight += min_w
        S.add(j)
    print(weight)
    print(*edges, sep="\n")
