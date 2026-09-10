"""
[복습 02 - 배열/리스트 다루기]  (Week2 / 02_array)

핵심 개념:
- 인덱스 접근은 O(1), 중간 삽입/삭제는 O(n).
- 슬라이싱은 새 리스트를 만든다 (원본 불변, 메모리 O(n)).
- '한 번만 훑으면서 답을 유지하는' 패턴(카데인)과
  '두 개의 포인터를 같이 옮기는' 패턴(병합)은 매우 자주 쓰인다.

문제:
1) rotate(arr, k)
   - 오른쪽으로 k칸 회전한 '새 리스트'를 반환 (원본은 그대로)
   - k 가 길이보다 클 수 있다. 빈 리스트면 빈 리스트
   - [1,2,3,4,5], k=2 -> [4,5,1,2,3]

2) max_subarray_sum(arr)
   - 연속된 부분 배열의 합 중 최댓값 (카데인 알고리즘, O(n))
   - 원소가 전부 음수면 그중 가장 큰 값. 빈 리스트면 0
   - [-2,1,-3,4,-1,2,1,-5,4] -> 6  ([4,-1,2,1])

3) merge_sorted(a, b)
   - 이미 정렬된 두 리스트를 정렬 상태로 합친다 (투 포인터, O(n+m))
   - 합친 뒤 sort() 하면 O(n log n) 이라 반칙!
   - [1,3,5], [2,4,6] -> [1,2,3,4,5,6]

힌트:
- 1) k %= len(arr) 로 먼저 줄이고 슬라이싱 두 조각을 이어붙인다
- 2) cur = max(x, cur + x)  "여기서 새로 시작할까, 이어붙일까"
- 3) 한쪽이 먼저 끝나면 남은 쪽을 통째로 붙인다
"""

def rotate(arr, k):
    n = len(arr)
    if n == 0:
        return []
    k %= n
    return arr[n - k:] + arr[:n - k]


def max_subarray_sum(arr):
    if not arr:
        return 0
    best = cur = arr[0]
    for x in arr[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def merge_sorted(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


if __name__ == "__main__":
    print("=== 배열 회전 ===")
    base = [1, 2, 3, 4, 5]
    for k in [0, 1, 2, 5, 7]:
        print(f"{base} k={k} -> {rotate(base, k)}")
    print(f"원본 유지 확인: {base}")
    print(f"[] k=3 -> {rotate([], 3)}")
    print()

    print("=== 최대 연속 부분합 (카데인) ===")
    for arr in [[-2, 1, -3, 4, -1, 2, 1, -5, 4],
                [1, 2, 3, 4],
                [-5, -2, -9],
                [7],
                []]:
        print(f"{arr} -> {max_subarray_sum(arr)}")
    print()

    print("=== 정렬된 두 리스트 병합 ===")
    for a, b in [([1, 3, 5], [2, 4, 6]),
                 ([1, 2, 3], []),
                 ([], []),
                 ([1, 1, 2], [1, 3])]:
        print(f"{a} + {b} -> {merge_sorted(a, b)}")
