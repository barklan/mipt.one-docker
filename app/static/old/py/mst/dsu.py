def make_set(x):
    return x


def find_set(x):
    if dsu[x] == x:
        return x
    return find_set(dsu[x])


def union_sets(x, y):
    x = find_set(x)
    y = find_set(y)
    if x != y:
        dsu[y] = x


dsu = [make_set(i) for i in range(n)]
