"""
[복습 10 - 이분 탐색]  (Week2 / 10_binary_search)

핵심 개념:
- 전제: 배열이 정렬되어 있어야 한다. 매 단계 후보가 절반 -> O(log n).
- 경계 조건이 전부다. 두 가지 형태를 구분해서 외우자.
  * 값 찾기:   lo <= hi,  hi = len-1,  mid±1 로 좁힘
  * 경계 찾기: lo <  hi,  hi = len,    hi = mid (mid를 버리지 않음)
- mid = (lo + hi) // 2 는 항상 lo 쪽으로 내려간다(내림). 그래서
  경계 탐색에서 lo = mid 로 쓰면 무한 루프가 난다.
- 파라메트릭 서치: "최적값을 구하라"를 "이 값이 가능한가?(예/아니오)"로 바꾸고
  답 자체를 이분 탐색한다. 가능하면 더 욕심내고, 불가능하면 물러선다.

문제:
1) binary_search(arr, target)
   - 정렬된 arr 에서 target 의 인덱스를 반환. 없으면 -1

2) lower_bound(arr, target)
   - target '이상'인 값이 처음 나오는 위치. 없으면 len(arr)
   - [1,2,2,2,3], 2 -> 1

3) upper_bound(arr, target)
   - target '초과'인 값이 처음 나오는 위치. 없으면 len(arr)
   - [1,2,2,2,3], 2 -> 4
   - upper_bound - lower_bound = target 의 개수

4) max_cut_length(trees, need)
   - 절단기 높이 H 를 정하면 나무마다 (높이 - H) 만큼 잘린 부분을 가져간다
   - need 미터 이상 가져갈 수 있는 H 의 '최댓값'을 반환 (H 는 0 이상 정수)
   - [20,15,10,17], need=7 -> 15   (5 + 2 = 7)

힌트:
- 1) while lo <= hi, 못 찾으면 -1
- 2) arr[mid] < target 이면 lo = mid + 1, 아니면 hi = mid
- 3) arr[mid] <= target 이면 lo = mid + 1, 아니면 hi = mid  (등호만 다르다!)
- 4) H 를 0 ~ max(trees) 범위에서 이분 탐색.
     충분히 가져갈 수 있으면 답을 기록하고 H 를 더 키운다
"""


def binary_search(arr, target):
    # TODO: lo, hi = 0, len(arr) - 1 로 시작
    pass


def lower_bound(arr, target):
    # TODO: lo, hi = 0, len(arr) 로 시작하고 hi = mid 로 좁힌다
    pass


def upper_bound(arr, target):
    # TODO: lower_bound 와 부등호 하나만 다르다
    pass


def max_cut_length(trees, need):
    # TODO: 높이 H 를 이분 탐색. sum(t - H for t in trees if t > H) >= need 이면 가능
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 이분 탐색 ===")
    arr = [1, 3, 5, 7, 9, 11]
    for target in [1, 7, 11, 4, 0, 100]:
        print(f"{arr} 에서 {target} -> {binary_search(arr, target)}")
    print(f"[] 에서 5 -> {binary_search([], 5)}")
    print()

    print("=== lower_bound / upper_bound ===")
    arr = [1, 2, 2, 2, 3, 5]
    for target in [0, 1, 2, 3, 4, 5, 6]:
        lo = lower_bound(arr, target)
        hi = upper_bound(arr, target)
        print(f"{arr} target={target} -> lower={lo}, upper={hi}, 개수={hi - lo}")
    print()

    print("=== 파라메트릭 서치 (나무 자르기) ===")
    for trees, need in [([20, 15, 10, 17], 7),
                        ([4, 42, 40, 26, 46], 20),
                        ([10], 10),
                        ([1, 2, 3], 100)]:
        h = max_cut_length(trees, need)
        got = sum(t - h for t in trees if t > h)
        print(f"나무={trees}, 필요={need} -> 높이={h} (실제 획득 {got}m)")
