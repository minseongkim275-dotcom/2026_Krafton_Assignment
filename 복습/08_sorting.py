"""
[복습 08 - 기본 정렬]  (Week2 / 08_bubble_sort)

핵심 개념:
- 선택 정렬: 남은 구간에서 최솟값을 찾아 맨 앞과 교환. 항상 O(n^2), 교환은 n-1번.
- 삽입 정렬: 앞쪽은 이미 정렬됐다고 보고, 새 원소를 자기 자리에 끼워넣는다.
  거의 정렬된 배열에서는 O(n) 에 가깝다.
- 버블 정렬: 인접한 두 개를 비교/교환. 한 패스에서 교환이 한 번도 없었다면
  이미 정렬된 것이므로 즉시 종료할 수 있다(조기 종료 최적화).
- 세 정렬 모두 최악 O(n^2). 실전에서는 O(n log n) 인 병합/퀵 정렬을 쓴다.

문제:
1) selection_sort(arr)
   - 선택 정렬로 오름차순 정렬한 '새 리스트' 반환 (원본 유지)

2) insertion_sort(arr)
   - 삽입 정렬로 오름차순 정렬한 '새 리스트' 반환 (원본 유지)

3) bubble_sort_passes(arr)
   - 버블 정렬 + 조기 종료. (정렬된 리스트, 실제 수행한 패스 수) 튜플 반환
   - 이미 정렬된 [1,2,3,4] 는 1번의 패스만에 끝나야 한다
   - 원소가 1개 이하면 패스 0

힌트:
- 1) 바깥 i, 안쪽 j 로 최솟값 인덱스를 찾고 a[i] 와 교환
- 2) key = a[i] 를 빼두고, 그보다 큰 값들을 오른쪽으로 한 칸씩 민다
- 3) swapped 플래그를 두고, 패스가 끝났는데 False 면 break
"""


def selection_sort(arr):
    # TODO: 원본을 건드리지 않도록 a = list(arr) 로 복사부터
    # TODO: 남은 구간의 최솟값 인덱스를 찾아 교환
    pass


def insertion_sort(arr):
    # TODO: i번째 값을 앞쪽 정렬된 구간의 알맞은 자리에 끼워넣기
    pass


def bubble_sort_passes(arr):
    # TODO: 인접 비교/교환 + swapped 플래그로 조기 종료
    # TODO: (정렬 결과, 패스 수) 를 반환
    pass


# 테스트 케이스
if __name__ == "__main__":
    samples = [
        [5, 2, 9, 1, 5, 6],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [42],
        [],
        [3, 3, 3],
    ]

    print("=== 선택 정렬 ===")
    for arr in samples:
        print(f"{arr} -> {selection_sort(arr)}")
    print()

    print("=== 삽입 정렬 ===")
    for arr in samples:
        print(f"{arr} -> {insertion_sort(arr)}")
    print()

    print("=== 버블 정렬 (조기 종료) ===")
    for arr in samples:
        sorted_arr, passes = bubble_sort_passes(arr)
        print(f"{arr} -> {sorted_arr} (패스 {passes}회)")
    print()

    print("=== 원본 보존 확인 ===")
    original = [3, 1, 2]
    selection_sort(original)
    insertion_sort(original)
    bubble_sort_passes(original)
    print(f"원본: {original}")
    print()

    print("=== 세 정렬 결과가 서로 같은지 ===")
    for arr in samples:
        a = selection_sort(arr)
        b = insertion_sort(arr)
        c, _ = bubble_sort_passes(arr)
        print(f"{arr}: {a == b == c == sorted(arr)}")
