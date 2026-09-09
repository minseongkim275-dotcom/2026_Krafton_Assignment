"""
[복습 11 - 분할 정복]  (Week2 / 11_divide_conquer, 01_quick_sort, 02_merge_sort)

핵심 개념:
- Divide(쪼개고) - Conquer(각각 풀고) - Combine(합친다)
- 병합 정렬: 반으로 쪼개고 -> 각각 정렬 -> 두 정렬된 배열을 병합.
  항상 O(n log n), 추가 메모리 O(n), 안정 정렬.
- 퀵 정렬: 피벗을 정하고 -> 작은 것/같은 것/큰 것으로 나누고 -> 양쪽을 정렬.
  평균 O(n log n) 이지만 피벗이 항상 최소/최대면 최악 O(n^2).
  (이미 정렬된 배열에서 첫 원소를 피벗으로 쓰면 최악이 된다)
- 재귀 깊이가 log n 이 되려면 '반씩' 줄어야 한다는 게 포인트.

문제:
1) merge_sort(arr)
   - 병합 정렬로 정렬한 새 리스트 반환 (원본 유지)
   - 합치는 부분(merge)은 02번에서 만든 투 포인터와 같다

2) quick_sort(arr)
   - 퀵 정렬로 정렬한 새 리스트 반환
   - 피벗은 가운데 원소(arr[len//2])를 쓰고, less/equal/greater 세 덩어리로 나눈다
   - 중복 값이 있어도 무한 재귀에 빠지지 않아야 한다

3) max_subarray_dc(arr)
   - 최대 연속 부분합을 '분할 정복'으로 구한다 (02번은 카데인, 이번엔 O(n log n))
   - 답은 세 가지 중 최댓값:
       (a) 왼쪽 절반 안에만 있는 경우
       (b) 오른쪽 절반 안에만 있는 경우
       (c) 가운데를 걸치는 경우 -> mid에서 왼쪽으로 뻗은 최대합 + 오른쪽으로 뻗은 최대합
   - 빈 리스트면 0

힌트:
- 1) 길이가 1 이하면 그대로 반환 (base case)
- 2) [x for x in arr if x < pivot] 처럼 세 리스트로 나눈다
- 3) (c)는 반드시 mid를 포함해야 하므로 mid부터 바깥으로 누적합을 늘려가며 최댓값
"""

def merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def quick_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


def max_subarray_dc(arr):
    if not arr:
        return 0

    def solve(lo, hi):
        if lo == hi:
            return arr[lo]
        mid = (lo + hi) // 2
        left = solve(lo, mid)
        right = solve(mid + 1, hi)

        best_left = arr[mid]
        total = 0
        for i in range(mid, lo - 1, -1):
            total += arr[i]
            best_left = max(best_left, total)

        best_right = arr[mid + 1]
        total = 0
        for i in range(mid + 1, hi + 1):
            total += arr[i]
            best_right = max(best_right, total)

        return max(left, right, best_left + best_right)

    return solve(0, len(arr) - 1)


if __name__ == "__main__":
    samples = [
        [5, 2, 9, 1, 5, 6],
        [38, 27, 43, 3, 9, 82, 10],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 3, 3, 3],
        [42],
        [],
    ]

    print("=== 병합 정렬 ===")
    for arr in samples:
        print(f"{arr} -> {merge_sort(arr)}")
    print()

    print("=== 퀵 정렬 ===")
    for arr in samples:
        print(f"{arr} -> {quick_sort(arr)}")
    print()

    print("=== 정렬 결과 검증 ===")
    for arr in samples:
        print(f"{arr}: {merge_sort(arr) == quick_sort(arr) == sorted(arr)}")
    print()

    print("=== 최대 연속 부분합 (분할 정복) ===")
    for arr in [[-2, 1, -3, 4, -1, 2, 1, -5, 4],
                [1, 2, 3, 4],
                [-5, -2, -9],
                [7],
                []]:
        print(f"{arr} -> {max_subarray_dc(arr)}")
