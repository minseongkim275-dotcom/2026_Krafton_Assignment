# 복습 문제 (Week2 + Week3)

week2 / week3 에서 다룬 개념을 다시 짚는 20문제입니다.
각 파일은 원본 문제와 같은 형식입니다 — docstring에 개념 정리 + 문제 설명이 있고,
`TODO` 가 달린 함수 본문을 채운 뒤 실행하면 됩니다.

## 사용법

```bash
python check.py            # 전체 채점
python check.py 01         # 1번만 채점
python check.py --list     # 문제 목록
python check.py --diff 01  # 틀린 줄 전부 보기
```

채점은 문제 파일을 실행한 출력을 `NN_xxx_output.txt` 와 줄 단위로 비교합니다.
정답 코드는 `정답/` 폴더에 있습니다. 막혔을 때만 열어보세요.

## 문제 목록

### Week2 복습

| # | 파일 | 다루는 개념 |
|---|------|------------|
| 01 | `01_string.py` | 문자열 불변성, 투 포인터, join으로 O(n) 이어붙이기 |
| 02 | `02_array.py` | 슬라이싱, 카데인 알고리즘, 투 포인터 병합 |
| 03 | `03_hash_dict.py` | dict/set O(1) 조회, "무엇을 key로 삼을까" |
| 04 | `04_brute_force.py` | 경우의 수 계산, 비트마스크 부분집합 |
| 05 | `05_recursion.py` | base case / recursive case, 분할정복 거듭제곱, 하노이 |
| 06 | `06_backtracking.py` | 선택-재귀-되돌리기, 가지치기, N-Queen |
| 07 | `07_complexity.py` | 빅오 표기, 반복 횟수 세기, 복잡도 퀴즈 |
| 08 | `08_sorting.py` | 선택/삽입/버블 정렬, 버블의 조기 종료 |
| 09 | `09_number_theory.py` | O(√n) 소수 판별, 에라토스테네스, 유클리드 호제법 |
| 10 | `10_binary_search.py` | lower/upper bound 경계 처리, 파라메트릭 서치 |
| 11 | `11_divide_conquer.py` | 병합/퀵 정렬, 분할정복 최대 부분합 |
| 12 | `12_stack.py` | 괄호 검사, 후위 표기식, 모노토닉 스택 |
| 13 | `13_queue_deque.py` | deque가 필요한 이유, 요세푸스, 슬라이딩 윈도우 |
| 14 | `14_linked_list.py` | 링크 뒤집기, slow/fast 투 포인터, 사이클 감지 |
| 15 | `15_heap.py` | sift up/down 직접 구현, 크기 k 힙, k-way 병합 |

### Week3 복습

| # | 파일 | 다루는 개념 |
|---|------|------------|
| 16 | `16_tree_bst.py` | 순회 3종 + 레벨 순회, BST 삽입, BST 유효성 검사 |
| 17 | `17_graph_bfs_dfs.py` | 인접 행렬/리스트, BFS 최단거리, DFS, 섬 개수 |
| 18 | `18_dp.py` | 메모이제이션 vs 타뷸레이션, 계단, 0/1 배낭, LIS |
| 19 | `19_greedy.py` | 그리디가 틀리는 반례, 회의실 배정 |
| 20 | `20_advanced.py` | 위상 정렬, 다익스트라, LCS 역추적 |

## 특히 헷갈리기 쉬운 것들

- **이분 탐색 경계** (10번): `lo <= hi` + `hi = mid ± 1` 과 `lo < hi` + `hi = mid` 를 구분할 것
- **BST 유효성** (16번): 부모하고만 비교하면 안 되고, 조상 전체의 범위를 물려받아야 한다
- **BFS 방문 표시** (17번): 큐에서 꺼낼 때가 아니라 **넣을 때** 표시해야 중복이 안 생긴다
- **0/1 배낭** (18번): 1차원 dp는 무게를 **큰 쪽부터** 갱신해야 물건이 한 번만 담긴다
- **백트래킹 복사** (06번): 결과에 넣을 때 `path` 가 아니라 `tuple(path)` / `path[:]`
- **list.pop(0)** (13번): O(n)이다. 큐가 필요하면 무조건 `deque`
