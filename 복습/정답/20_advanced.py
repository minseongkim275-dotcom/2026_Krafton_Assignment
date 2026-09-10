"""
[복습 20 - 위상 정렬 / 다익스트라 / LCS]  (Week3 advanced 전체)

핵심 개념:
- 위상 정렬: 방향 그래프에서 '선행 관계'를 어기지 않는 순서.
  진입 차수(indegree)가 0인 정점부터 꺼내고, 꺼낼 때마다 이웃의 차수를 1 줄인다.
  모든 정점을 못 꺼내면 사이클이 있다는 뜻. DAG 에서만 가능.
- 다익스트라: 음이 아닌 가중치 그래프의 단일 시작점 최단 경로. O((V+E) log V).
  "지금까지 확정된 것 중 가장 가까운 정점"을 우선순위 큐로 고른다.
  음수 간선이 있으면 쓸 수 없다(한 번 확정한 걸 뒤집어야 하므로).
  이미 확정된 정점이 큐에서 또 나오면 건너뛰는 처리가 필요하다.
- LCS(최장 공통 부분 수열): 연속일 필요는 없다.
  dp[i][j] = a의 앞 i글자와 b의 앞 j글자의 LCS 길이
    a[i-1] == b[j-1] 이면  dp[i-1][j-1] + 1
    아니면                max(dp[i-1][j], dp[i][j-1])

문제:
1) topological_sort(n, edges)
   - 정점은 0 ~ n-1, edges 는 (u, v) 이며 'u 를 먼저' 해야 한다는 뜻
   - 가능한 순서 중 '사전순으로 가장 빠른' 것을 리스트로 반환
   - 사이클이 있어서 불가능하면 None
   - 사전순을 위해서는 큐 대신 최소 힙(heapq)을 쓴다

2) dijkstra(n, edges, start)
   - edges 는 (u, v, w) 방향 간선. start 에서 각 정점까지의 최단 거리 리스트
   - 도달할 수 없으면 -1

3) lcs_length(a, b) / lcs_string(a, b)
   - LCS 의 길이와, 실제 LCS 문자열 하나를 반환
   - 역추적 규칙(답을 하나로 정하기 위해 고정):
       글자가 같으면 -> 대각선으로 이동하며 그 글자를 앞에 붙인다
       다르면 dp[i-1][j] >= dp[i][j-1] 이면 위로, 아니면 왼쪽으로
   - "ACAYKP", "CAPCAK" -> 길이 4

힌트:
- 1) indeg 배열과 인접 리스트를 만들고, heapq.heappush/heappop
- 2) dist 배열을 INF 로 채우고 dist[start]=0, 힙에 (거리, 정점)
- 3) (len(a)+1) x (len(b)+1) 표를 만든다. 0행/0열은 0
"""

import heapq


def topological_sort(n, edges):
    indeg = [0] * n
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    heap = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    return order if len(order) == n else None


def dijkstra(n, edges, start):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return [-1 if d == INF else d for d in dist]


def _lcs_table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs_length(a, b):
    return _lcs_table(a, b)[len(a)][len(b)]


def lcs_string(a, b):
    dp = _lcs_table(a, b)
    i, j = len(a), len(b)
    out = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(out))


if __name__ == "__main__":
    print("=== 위상 정렬 ===")
    cases = [
        (6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]),
        (3, [(0, 1), (1, 2)]),
        (3, [(0, 1), (1, 2), (2, 0)]),   # 사이클
        (4, []),                          # 간선 없음
        (1, []),
    ]
    for n, edges in cases:
        print(f"n={n}, edges={edges}")
        print(f"  -> {topological_sort(n, edges)}")
    print()

    print("=== 다익스트라 ===")
    #  0 -1-> 1 -2-> 2
    #  0 -4-------> 2
    #  3 은 고립
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 1, 1)]
    for start in [0, 1, 3]:
        print(f"start={start} -> {dijkstra(4, edges, start)}")

    edges2 = [(0, 1, 10), (0, 2, 3), (2, 1, 4), (1, 3, 2), (2, 3, 8), (3, 4, 5)]
    print(f"큰 예제 start=0 -> {dijkstra(5, edges2, 0)}")
    print(f"간선 없음 -> {dijkstra(3, [], 0)}")
    print()

    print("=== LCS ===")
    pairs = [
        ("ACAYKP", "CAPCAK"),
        ("AAA", "AAA"),
        ("ABC", "DEF"),
        ("", "ABC"),
        ("ABCBDAB", "BDCABA"),
        ("python", "typhon"),
    ]
    for a, b in pairs:
        print(f"{a!r} vs {b!r} -> 길이 {lcs_length(a, b)}, LCS {lcs_string(a, b)!r}")
