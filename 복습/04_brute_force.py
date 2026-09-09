"""
[복습 04 - 완전탐색(브루트 포스)]  (Week2 / 04_brute_force)

핵심 개념:
- 가능한 모든 경우를 빠짐없이, 중복 없이 만들어보고 조건을 확인한다.
- 경우의 수를 먼저 계산해서 시간 안에 되는지 판단하는 게 먼저다.
  * 부분집합: 2^n   * 순열: n!   * 두 개 뽑기: nC2 = n(n-1)/2
- 비트마스크: 0 ~ 2^n - 1 을 돌면서 i번째 비트가 켜져 있으면 i번째 원소 선택.
  (mask >> i) & 1  또는  mask & (1 << i)

문제:
1) subset_sum(nums, target)
   - 부분집합 중 합이 target 인 것이 있는지 True/False (비트마스크 완전탐색)
   - 공집합(합 0)도 부분집합에 포함한다
   - [3,34,4,12,5,2], 9 -> True  (4+5)

2) max_pair_product(nums)
   - 서로 다른 두 원소를 골라 곱한 값 중 최댓값
   - 음수 × 음수가 최대일 수 있으니 정렬 대신 이중 반복으로 전부 확인
   - 원소가 2개 미만이면 None

3) count_triplets(nums, target)
   - 서로 다른 세 인덱스 i < j < k 의 합이 target 인 조합의 개수
   - [1,2,3,4,5], 9 -> 2  ((1,3,5), (2,3,4))

힌트:
- 1) for mask in range(1 << n): 안에서 켜진 비트만 더한다
- 2) for i ... for j in range(i+1, n)
- 3) 삼중 반복. 인덱스 범위를 i<j<k 로 잡으면 중복이 안 생긴다
"""


def subset_sum(nums, target):
    # TODO: 0 ~ 2^n - 1 의 mask 를 돌면서 부분집합 합을 구한다
    pass


def max_pair_product(nums):
    # TODO: 모든 (i, j) 쌍을 확인해서 최댓값 갱신
    pass


def count_triplets(nums, target):
    # TODO: i < j < k 인 모든 조합을 세어본다
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 부분집합 합 ===")
    for nums, target in [([3, 34, 4, 12, 5, 2], 9),
                         ([3, 34, 4, 12, 5, 2], 30),
                         ([1, 2, 3], 0),
                         ([], 5)]:
        print(f"{nums}, target={target} -> {subset_sum(nums, target)}")
    print()

    print("=== 두 수의 최대 곱 ===")
    for nums in [[1, 5, 3, 9],
                 [-10, -9, 1, 2],
                 [-1, 0, 1],
                 [7],
                 []]:
        print(f"{nums} -> {max_pair_product(nums)}")
    print()

    print("=== 합이 target 인 세 수의 조합 개수 ===")
    for nums, target in [([1, 2, 3, 4, 5], 9),
                         ([0, 0, 0, 0], 0),
                         ([1, 2, 3], 10),
                         ([-1, 0, 1, 2, -1], 0)]:
        print(f"{nums}, target={target} -> {count_triplets(nums, target)}")
