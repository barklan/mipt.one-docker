def get_key(x):
    return x[2]


if __name__ == "__main__":
    n, m = map(int, input().split())
    a = []
    for i in range(m):
        u, v, w = map(int, input().split())
        a.append((u, v, w))
    a.sort(key=get_key)
    tree_id = [i for i in range(n)]
    edges = []
    weight = 0
    for u, v, w in a:
        if tree_id[u] != tree_id[v]:
            weight += w
            edges.append((u, v, w))
            j = tree_id[v]
            for i in range(n):
                if tree_id[i] == j:
                    tree_id[i] = tree_id[u]
    print(weight)
    print(*edges, sep="\n")
