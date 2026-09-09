"""
[복습 17 - 그래프 표현과 탐색]  (Week3 / 03_graph_basic, 04_bfs, 05_dfs)

핵심 개념:
- 인접 행렬: 공간 O(V^2), 두 정점의 연결 확인 O(1). 정점 수가 적고 간선이 많을 때.
- 인접 리스트: 공간 O(V+E), 이웃 순회가 빠르다. 보통은 이쪽.
- BFS(큐): 가까운 곳부터. 간선 가중치가 모두 같을 때 '최단 거리'를 보장한다.
- DFS(스택/재귀): 한 방향으로 끝까지. 경로 탐색, 연결 요소, 사이클 판별에.
- 둘 다 방문 체크가 핵심. BFS 는 '큐에 넣는 순간' 방문 표시를 해야 한다.
  꺼낼 때 표시하면 같은 정점이 큐에 여러 번 들어간다.

문제:
1) to_adj_list(matrix)
   - 인접 행렬(0/1 2차원 리스트)을 인접 리스트 {정점: [이웃...]} 로 변환
   - 이웃은 번호 오름차순. 연결이 없는 정점도 빈 리스트로 넣는다

2) bfs_distance(graph, start)
   - start 에서 각 정점까지의 최단 거리(간선 개수)를 {정점: 거리} 로 반환
   - 도달할 수 없는 정점은 결과에 넣지 않는다. start 자신은 0

3) dfs_order(graph, start)
   - DFS 방문 순서를 리스트로 반환 (이웃은 graph 에 적힌 순서대로)

4) count_islands(grid)
   - 0과 1로 된 2차원 격자에서 1이 상하좌우로 이어진 덩어리(섬)의 개수
   - 대각선은 연결로 치지 않는다

힌트:
- 1) matrix[i][j] == 1 이면 i 의 이웃에 j 추가
- 2) BFS 하면서 dist[다음] = dist[현재] + 1
- 3) 재귀로 visited 를 공유하며 내려간다
- 4) 아직 방문 안 한 1을 만나면 개수 +1 하고, 거기서 BFS/DFS 로 그 섬을 전부 지운다
"""

from collections import deque


def to_adj_list(matrix):
    # TODO: 행 i, 열 j 를 돌면서 1인 곳을 이웃으로
    pass


def bfs_distance(graph, start):
    # TODO: 큐에 넣는 순간 거리를 기록
    pass


def dfs_order(graph, start):
    # TODO: 재귀로 방문 순서를 쌓는다
    pass


def count_islands(grid):
    # TODO: 모든 칸을 훑으면서 방문 안 한 1에서 탐색을 시작
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 인접 행렬 -> 인접 리스트 ===")
    matrix = [
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
    ]
    graph = to_adj_list(matrix)
    for v in sorted(graph):
        print(f"  {v}: {graph[v]}")
    print(f"고립 정점 포함: {to_adj_list([[0, 0], [0, 0]])}")
    print()

    #  0 --- 1        4 --- 5
    #  |  /  |
    #  2 --- 3
    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [1, 2],
        4: [5],
        5: [4],
    }

    print("=== BFS 최단 거리 ===")
    for start in [0, 3, 4]:
        print(f"start={start} -> {bfs_distance(graph, start)}")
    print()

    print("=== DFS 방문 순서 ===")
    for start in [0, 3, 4]:
        print(f"start={start} -> {dfs_order(graph, start)}")
    print()

    print("=== BFS 와 DFS 는 방문 '집합'은 같아야 한다 ===")
    for start in [0, 4]:
        bfs_set = set(bfs_distance(graph, start))
        dfs_set = set(dfs_order(graph, start))
        print(f"start={start}: {bfs_set == dfs_set}")
    print()

    print("=== 섬의 개수 ===")
    grids = [
        [[1, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]],

        [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]],

        [[0, 0],
         [0, 0]],

        [[1, 0, 1],
         [0, 1, 0],
         [1, 0, 1]],

        [],
    ]
    for grid in grids:
        print(f"{grid} -> {count_islands(grid)}개")
