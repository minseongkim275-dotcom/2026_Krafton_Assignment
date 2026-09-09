"""
[복습 19 - 그리디]  (Week3 / 08_greedy_coin, 09_greedy_meeting)

핵심 개념:
- 매 순간 가장 좋아 보이는 것을 고르고, 되돌아보지 않는다.
- 빠르지만 '항상 최적'은 아니다. 그리디가 옳으려면 증명이 필요하다.
  * 동전: 400원, 500원, 900원짜리로 1300원을 만들 때 -> 900+400 = 2개.
    그런데 코인이 [1,3,4] 이고 6원이면 그리디는 4+1+1 = 3개, 최적은 3+3 = 2개.
    -> 큰 동전이 작은 동전의 배수 관계일 때만 그리디가 안전하다.
  * 회의실: '끝나는 시간이 빠른 것부터' 고르면 최적임이 증명된다.
    (시작이 빠른 순, 회의 시간이 짧은 순은 둘 다 반례가 있다)
- 그리디가 틀리는 문제는 대개 DP 로 풀린다.

문제:
1) coin_change_greedy(coins, amount)
   - 큰 동전부터 최대한 쓰는 방식으로 필요한 동전 개수를 반환
   - 정확히 만들지 못하면 -1

2) coin_change_dp(coins, amount)
   - 실제 최소 동전 개수를 DP 로 (그리디의 답과 비교해보기 위함)
   - 만들 수 없으면 -1

3) max_meetings(meetings)
   - (시작, 끝) 회의 목록에서 겹치지 않게 최대 몇 개를 배정할 수 있는지
   - 끝나는 시간이 같으면 시작이 빠른 것부터. 앞 회의가 끝나는 시각에
     바로 시작하는 회의는 배정할 수 있다 (끝 <= 시작)
   - [(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11)] -> 3
     ((1,4) -> (5,7) -> (8,11))

힌트:
- 1) sorted(coins, reverse=True) 로 돌면서 amount // coin
- 2) dp[i] = i원을 만드는 최소 동전 수, dp[0] = 0
- 3) 끝나는 시간 기준 정렬 후, 마지막으로 배정한 회의의 끝 시각만 기억하면 된다
"""

def coin_change_greedy(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        if amount <= 0:
            break
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1


def coin_change_dp(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
    return dp[amount] if dp[amount] != INF else -1


def max_meetings(meetings):
    count = 0
    last_end = None
    for start, end in sorted(meetings, key=lambda m: (m[1], m[0])):
        if last_end is None or start >= last_end:
            count += 1
            last_end = end
    return count


if __name__ == "__main__":
    print("=== 동전 거스름돈: 그리디 vs DP ===")
    cases = [
        ([500, 100, 50, 10], 1260),
        ([1, 5, 10, 25], 63),
        ([1, 3, 4], 6),        # 그리디가 틀리는 유명한 반례
        ([1, 7, 10], 14),      # 여기도 반례
        ([2], 3),              # 만들 수 없음
        ([5, 2], 0),
    ]
    for coins, amount in cases:
        g = coin_change_greedy(coins, amount)
        d = coin_change_dp(coins, amount)
        mark = "일치" if g == d else "그리디 실패!"
        print(f"coins={coins}, amount={amount} -> 그리디 {g}개 / 최적 {d}개  ({mark})")
    print()

    print("=== 회의실 배정 ===")
    meeting_cases = [
        [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)],
        [(1, 2), (2, 3), (3, 4)],
        [(0, 10), (1, 2), (2, 3)],
        [(1, 1), (1, 1), (2, 2)],
        [(5, 6)],
        [],
    ]
    for meetings in meeting_cases:
        print(f"{meetings} -> {max_meetings(meetings)}개")
