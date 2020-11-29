def sift_up(i):
    while i > 0 and heap[(i - 1) // 2][2] > heap[i][2]:
        v2h[heap[i][1]], v2h[heap[(i - 1) // 2][1]] = (i - 1) // 2, i
        heap[i], heap[(i - 1) // 2] = heap[(i - 1) // 2], heap[i]
        i = (i - 1) // 2


def sift_down(i):
    n = len(heap)
    while i * 2 + 1 < n:
        j = i
        if heap[i][2] > heap[i * 2 + 1][2]:
            j = i * 2 + 1
        if i * 2 + 2 < n and heap[j][2] > heap[i * 2 + 2][2]:
            j = i * 2 + 2
        if i == j:
            break
        v2h[heap[i][1]], v2h[heap[j][1]] = j, i
        heap[i], heap[j] = heap[j], heap[i]
        i = j


def extract_min():
    x = heap[0]
    v2h[x[1]] = -1
    tmp = heap.pop()
    if heap:
        heap[0] = tmp
        v2h[heap[0][1]] = 0
        sift_down(0)
    return x


def heapify():
    from math import ceil
    for i in range(ceil(len(heap) / 2), -1, -1):
        sift_down(i)


if __name__ == "__main__":
    n, m = map(int, input().split())
    a = {i: set() for i in range(n)}
    for i in range(m):
        u, v, w = map(int, input().split())
        a[u].add((v, w))
        a[v].add((u, w))
    heap = [(i, i, float("inf")) for i in range(1, n)]
    v2h = [-1] + [i-1 for i in range(1, n)]
    for v, w in a[0]:
        heap[v2h[v]] = (0, v, w)
    heapify()
    edges = []
    weight = 0
    for _ in range(n - 1):
        u, j, w = extract_min()
        edges.append((u, j, w))
        weight += w
        for v, w in a[j]:
            if v2h[v] != -1 and w < heap[v2h[v]][2]:
                heap[v2h[v]] = (j, v, w)
                sift_up(v2h[v])
    print(weight)
    print(*edges, sep="\n")
