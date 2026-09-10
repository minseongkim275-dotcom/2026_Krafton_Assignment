"""
[복습 18 - 동적 계획법(DP)]  (Week3 / 06_dp_fibonacci, 07_dp_stairs, 02_lcs)

핵심 개념:
- DP 를 쓸 수 있는 조건 두 가지
  1) 최적 부분 구조: 큰 문제의 답이 작은 문제의 답으로 만들어진다
  2) 중복 부분 문제: 같은 작은 문제를 여러 번 다시 푼다
- 두 가지 구현 방식
  * 메모이제이션(top-down): 재귀 + 캐시. 점화식 그대로라 쓰기 쉽다.
  * 타뷸레이션(bottom-up): 반복문으로 표를 채운다. 재귀 깊이 걱정이 없다.
- 순수 재귀 피보나치는 O(2^n), 메모이제이션을 붙이면 O(n).
  같은 점화식인데 '기억하느냐'만으로 복잡도가 통째로 바뀐다.
- DP 문제는 항상 "dp[i] 가 무엇을 뜻하는가"를 한 문장으로 먼저 정의할 것.

문제:
1) fib_memo(n)
   - 메모이제이션으로 n번째 피보나치. fib(0)=0, fib(1)=1
   - n=50 도 순식간에 나와야 한다

2) fib_tab(n)
   - 반복문(타뷸레이션)으로 같은 값을. 변수 두 개만 써서 공간 O(1)

3) climb_stairs(n)
   - 한 번에 1칸 또는 2칸씩 올라갈 때, n칸을 오르는 방법의 수
   - dp[i] = dp[i-1] + dp[i-2],  dp[0]=1, dp[1]=1
   - n=5 -> 8

4) knapsack(weights, values, capacity)
   - 0/1 배낭. 각 물건은 최대 한 번만. 담을 수 있는 최대 가치
   - dp[w] = 무게 w 까지 담았을 때의 최대 가치
   - 주의: 1차원 배열로 풀 때는 무게를 '큰 쪽부터' 갱신해야 한 번만 담긴다

5) lis_length(nums)
   - 최장 증가 부분 수열(LIS)의 길이. 연속이 아니어도 된다
   - dp[i] = i 번째로 '끝나는' LIS 의 길이 -> O(n^2)
   - [10,9,2,5,3,7,101,18] -> 4  ([2,3,7,101])

힌트:
- 1) 캐시 딕셔너리를 함수 밖 또는 기본 인자로 두고 있으면 바로 반환
- 3) 계단 문제는 피보나치와 사실상 같다. 초기값만 다르다
- 4) for i in 물건: for w in range(capacity, weight-1, -1)
- 5) 모든 j < i 에 대해 nums[j] < nums[i] 면 dp[i] = max(dp[i], dp[j]+1)
"""

_fib_cache = {}


def fib_memo(n):
    if n in _fib_cache:
        return _fib_cache[n]
    if n < 2:
        return n
    _fib_cache[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return _fib_cache[n]


def fib_tab(n):
    if n < 2:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur


def climb_stairs(n):
    if n < 2:
        return 1
    prev, cur = 1, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur


def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]


def lis_length(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


if __name__ == "__main__":
    print("=== 피보나치 (메모이제이션) ===")
    for n in [0, 1, 2, 10, 30, 50, 90]:
        print(f"fib({n}) = {fib_memo(n)}")
    print()

    print("=== 피보나치 (타뷸레이션) ===")
    print(f"두 방식이 같은가: {[fib_memo(i) for i in range(20)] == [fib_tab(i) for i in range(20)]}")
    print(f"fib_tab(100) = {fib_tab(100)}")
    print()

    print("=== 계단 오르기 ===")
    for n in [0, 1, 2, 3, 5, 10, 45]:
        print(f"{n}칸 -> {climb_stairs(n)}가지")
    print()

    print("=== 0/1 배낭 ===")
    cases = [
        ([1, 3, 4, 5], [1, 4, 5, 7], 7),
        ([2, 3, 4], [3, 4, 5], 5),
        ([10], [100], 5),
        ([1, 1, 1], [10, 20, 30], 2),
        ([], [], 10),
    ]
    for weights, values, capacity in cases:
        print(f"무게={weights}, 가치={values}, 용량={capacity} -> {knapsack(weights, values, capacity)}")
    print()

    print("=== 최장 증가 부분 수열 ===")
    for nums in [[10, 9, 2, 5, 3, 7, 101, 18],
                 [1, 2, 3, 4, 5],
                 [5, 4, 3, 2, 1],
                 [7, 7, 7],
                 [3],
                 []]:
        print(f"{nums} -> {lis_length(nums)}")
