"""
[복습 15 - 힙 / 우선순위 큐]  (Week2 / 03_priority_queue)

핵심 개념:
- 힙은 '완전 이진 트리'를 배열 하나로 표현한 것.
  0-based 에서  부모 = (i-1)//2,  왼쪽 = 2i+1,  오른쪽 = 2i+2
- 최소 힙의 규칙은 '부모 <= 자식' 딱 하나. 형제끼리는 순서가 없다.
  그래서 전체 정렬은 아니지만 최솟값은 항상 루트에 있다.
- push: 맨 뒤에 넣고 부모와 비교하며 올린다(sift up) -> O(log n)
- pop : 루트를 빼고 마지막 원소를 루트로 올린 뒤 내린다(sift down) -> O(log n)
- 정렬은 O(n log n) 이지만, "최솟값만 계속 꺼내면 될 때"는 힙이 훨씬 싸다.

문제:
1) heap_push(heap, x) / heap_pop(heap)
   - 파이썬 리스트를 최소 힙으로 쓰는 두 함수를 직접 구현
   - heap 은 제자리에서 수정(in-place). heap_pop 은 최솟값을 반환
   - 빈 힙에서 pop 하면 IndexError
   - heapq 모듈을 쓰지 말고 직접!

2) kth_largest(nums, k)
   - k번째로 큰 값을 반환. 크기 k 인 최소 힙을 유지하면 O(n log k)
   - [3,2,1,5,6,4], k=2 -> 5
   - k 가 길이보다 크면 None

3) merge_k_sorted(lists)
   - 정렬된 리스트 여러 개를 하나의 정렬된 리스트로 합친다
   - 힙에 (값, 리스트번호, 원소번호) 를 넣으면 O(N log k)

힌트:
- 1) sift up: 부모보다 작으면 교환하며 위로.
     sift down: 두 자식 중 '더 작은' 쪽과 비교해서 교환하며 아래로
- 2) 힙 크기가 k 를 넘으면 heap_pop 으로 가장 작은 걸 버린다. 남은 루트가 답
- 3) 각 리스트의 첫 원소를 넣고 시작. 꺼낼 때마다 그 리스트의 다음 원소를 넣는다
"""

def heap_push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] < heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break


def heap_pop(heap):
    if not heap:
        raise IndexError('힙이 비어있습니다')
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i = 0
        n = len(heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and heap[left] < heap[smallest]:
                smallest = left
            if right < n and heap[right] < heap[smallest]:
                smallest = right
            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
    return top


def kth_largest(nums, k):
    if k > len(nums) or k <= 0:
        return None
    heap = []
    for x in nums:
        heap_push(heap, x)
        if len(heap) > k:
            heap_pop(heap)
    return heap[0]


def merge_k_sorted(lists):
    heap = []
    for li, lst in enumerate(lists):
        if lst:
            heap_push(heap, (lst[0], li, 0))

    out = []
    while heap:
        value, li, ei = heap_pop(heap)
        out.append(value)
        if ei + 1 < len(lists[li]):
            heap_push(heap, (lists[li][ei + 1], li, ei + 1))
    return out


if __name__ == "__main__":
    print("=== 힙 push / pop ===")
    heap = []
    for x in [5, 3, 8, 1, 9, 2]:
        heap_push(heap, x)
        print(f"push {x} -> {heap}")
    print()

    print("꺼내는 순서 (정렬되어 나와야 함):")
    order = []
    while heap:
        order.append(heap_pop(heap))
    print(order)
    print()

    print("=== 힙 정렬 검증 ===")
    for nums in [[5, 1, 4, 1, 5, 9, 2, 6], [1], [], [3, 3, 3]]:
        h = []
        for x in nums:
            heap_push(h, x)
        out = [heap_pop(h) for _ in range(len(h))]
        print(f"{nums} -> {out} (일치: {out == sorted(nums)})")
    print()

    print("=== 빈 힙에서 pop ===")
    try:
        heap_pop([])
        print("예외가 발생하지 않았습니다")
    except IndexError:
        print("IndexError 발생 (정상)")
    print()

    print("=== k번째로 큰 값 ===")
    for nums, k in [([3, 2, 1, 5, 6, 4], 2),
                    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),
                    ([1], 1),
                    ([1, 2], 5)]:
        print(f"{nums}, k={k} -> {kth_largest(nums, k)}")
    print()

    print("=== 정렬된 리스트 k개 병합 ===")
    for lists in [[[1, 4, 5], [1, 3, 4], [2, 6]],
                  [[1, 2, 3]],
                  [[], [1], []],
                  []]:
        print(f"{lists} -> {merge_k_sorted(lists)}")
