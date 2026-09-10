"""
[복습 13 - 큐와 덱]  (Week2 / 13_queue)

핵심 개념:
- 큐는 FIFO (First In First Out).
- list.pop(0) 은 뒤의 원소를 전부 한 칸씩 당기므로 O(n)!
  반복문 안에서 쓰면 O(n^2) 가 된다. 반드시 collections.deque 를 쓸 것.
- deque 는 양쪽 끝 append/pop 이 O(1). rotate(k) 로 회전도 O(k).
- 덱에 '인덱스'를 넣고 값의 대소를 유지하는 기법(모노토닉 덱)으로
  슬라이딩 윈도우 최댓값을 O(n) 에 구할 수 있다.

문제:
1) josephus(n, k)
   - 1번부터 n번까지 원형으로 앉아 있고, k번째 사람을 차례로 제거한다
   - 제거되는 순서를 리스트로 반환
   - n=7, k=3 -> [3, 6, 2, 7, 5, 1, 4]

2) card_game(n)
   - 1~n 카드가 순서대로 쌓여있다. 맨 위 카드를 버리고,
     그 다음 카드를 맨 아래로 옮기는 것을 반복한다. 마지막 남는 카드는?
   - n=6 -> 4   (백준 2164 카드2)

3) sliding_window_max(nums, k)
   - 크기 k 인 창을 한 칸씩 옮기며 각 창의 최댓값을 리스트로 반환
   - 매번 max() 를 부르면 O(nk). 덱으로 O(n) 에 풀 것
   - [1,3,-1,-3,5,3,6,7], k=3 -> [3,3,5,5,6,7]

힌트:
- 1) deque 의 rotate(-(k-1)) 로 k번째를 맨 앞으로 보내고 popleft
- 2) popleft() 로 버리고, popleft() 한 것을 append()
- 3) 덱에 인덱스를 넣되, 새로 들어올 값보다 작은 값의 인덱스는 뒤에서 빼버린다.
     (더 최근에 더 큰 값이 왔으면 앞의 작은 값은 영원히 최댓값이 될 수 없다)
     창을 벗어난 앞쪽 인덱스는 popleft
"""

from collections import deque


def josephus(n, k):
    q = deque(range(1, n + 1))
    out = []
    while q:
        q.rotate(-(k - 1))
        out.append(q.popleft())
    return out


def card_game(n):
    q = deque(range(1, n + 1))
    while len(q) > 1:
        q.popleft()
        q.append(q.popleft())
    return q[0]


def sliding_window_max(nums, k):
    if not nums or k <= 0:
        return []
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


if __name__ == "__main__":
    print("=== 요세푸스 문제 ===")
    for n, k in [(7, 3), (5, 2), (4, 1), (1, 5)]:
        print(f"n={n}, k={k} -> {josephus(n, k)}")
    print()

    print("=== 카드2 ===")
    for n in [1, 2, 4, 6, 10, 100]:
        print(f"n={n} -> {card_game(n)}")
    print()

    print("=== 슬라이딩 윈도우 최댓값 ===")
    for nums, k in [([1, 3, -1, -3, 5, 3, 6, 7], 3),
                    ([1, 2, 3, 4, 5], 1),
                    ([5, 4, 3, 2, 1], 2),
                    ([9, 9, 9], 3),
                    ([], 3)]:
        print(f"{nums}, k={k} -> {sliding_window_max(nums, k)}")
    print()

    print("=== 무식하게 max() 쓴 결과와 비교 ===")
    nums = [4, 2, 12, 3, 8, 1, 9, 9, 5]
    for k in [1, 2, 3, 4]:
        brute = [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
        print(f"k={k}: {sliding_window_max(nums, k) == brute}")
