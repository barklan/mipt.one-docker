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


dsu = [make_set(i) for i in range(n)]
