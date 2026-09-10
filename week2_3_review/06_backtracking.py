"""
[복습 06 - 백트래킹]  (Week2 / 06_backtracking, 05_n_queen)

핵심 개념:
- 완전탐색 + 가지치기(pruning). 답이 될 가능성이 없으면 그 가지는 더 안 내려간다.
- 뼈대는 항상 같다:
    선택한다 -> 다음 단계로 내려간다(재귀) -> 선택을 되돌린다(백트래킹)
    path.append(x); backtrack(); path.pop()
- '되돌리기'를 빼먹으면 상태가 오염되어 전혀 다른 답이 나온다.
- 결과 리스트에 넣을 때는 반드시 복사본을 넣어야 한다.
  (path 를 그대로 넣으면 나중에 pop 되면서 같이 바뀐다 -> tuple(path) 또는 path[:])

문제:
1) permutations(nums)
   - nums 의 모든 순열을 튜플 리스트로 반환 (사전순으로 정렬)
   - [1,2,3] -> [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

2) combinations(nums, r)
   - nums 에서 r개를 고르는 모든 조합을 튜플 리스트로 반환
   - 입력 순서를 유지한다. r=0 이면 [()], r 이 길이보다 크면 []
   - [1,2,3,4], r=2 -> [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

3) n_queens(n)
   - n x n 체스판에 퀸 n개를 서로 공격하지 못하게 놓는 경우의 수
   - 같은 열, 같은 대각선에 있으면 안 된다
   - n=4 -> 2, n=8 -> 92

힌트:
- 1) used 배열로 이미 쓴 원소를 표시
- 2) 조합은 start 인덱스를 넘겨서 뒤쪽만 보게 하면 중복이 안 생긴다
- 3) 한 행에 하나씩 놓는다. 대각선 판별은
     ↘ 방향: row + col 이 같다 / ↙ 방향: row - col 이 같다
"""


def permutations(nums):
    # TODO: used 배열 + path 로 백트래킹
    # TODO: path 가 다 차면 tuple(path) 를 결과에 추가
    pass


def combinations(nums, r):
    # TODO: backtrack(start) 형태로 start 이후만 고른다
    pass


def n_queens(n):
    # TODO: row 를 0부터 n까지 내려가며 각 행에 퀸을 하나씩
    # TODO: 열/대각선 사용 여부를 배열로 관리하고, 되돌릴 때 해제
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 순열 ===")
    for nums in [[1, 2, 3], [1, 2], [7], []]:
        result = permutations(nums)
        print(f"{nums} -> {len(result)}개")
        print(f"  {result}")
    print()

    print("=== 조합 ===")
    for nums, r in [([1, 2, 3, 4], 2), ([1, 2, 3], 3), ([1, 2, 3], 0), ([1, 2], 5)]:
        result = combinations(nums, r)
        print(f"{nums}, r={r} -> {len(result)}개")
        print(f"  {result}")
    print()

    print("=== N-Queen ===")
    for n in range(1, 9):
        print(f"n={n} -> {n_queens(n)}가지")
