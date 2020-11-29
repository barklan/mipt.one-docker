def get_key(x):
    return x[2]


def make_set(x):
    return {
        "parent": x,
        "rank": 0
    }


def find_set(x):
    if dsu[x]["parent"] == x:
        return x
    dsu[x]["parent"] = find_set(dsu[x]["parent"])
    return dsu[x]["parent"]


def union_sets(x, y):
    x = find_set(x)
    y = find_set(y)
    if x != y:
        if dsu[x]["rank"] < dsu[y]["rank"]:
            x, y = y, x
        dsu[y]["parent"] = x
        if dsu[x]["rank"] == dsu[y]["rank"]:
            dsu[x]["rank"] += 1


if __name__ == "__main__":
    n, m = map(int, input().split())
    a = []
    for i in range(m):
        u, v, w = map(int, input().split())
        a.append((u, v, w))
    a.sort(key=get_key)
    dsu = [make_set(i) for i in range(n)]
    edges = []
    weight = 0
    for u, v, w in a:
        if find_set(u) != find_set(v):
            weight += w
            edges.append((u, v, w))
            union_sets(u, v)
    print(weight)
    print(*edges, sep="\n")
