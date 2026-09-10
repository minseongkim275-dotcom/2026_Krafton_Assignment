"""
[복습 05 - 재귀]  (Week2 / 05_recursion, 04_hanoi_tower)

핵심 개념:
- 재귀 함수는 두 부분으로만 이루어진다.
  1) base case  : 더 이상 쪼갤 수 없는 가장 작은 경우 (여기서 반드시 return)
  2) recursive case : 더 작은 문제로 넘기고 그 결과를 조합
- base case 를 빼먹으면 RecursionError (스택 오버플로).
- "더 작은 문제는 이미 풀렸다고 믿는다"가 재귀를 쓰는 요령.

문제:
1) flatten(lst)
   - 중첩 리스트를 1차원으로 펴서 새 리스트 반환
   - [1,[2,[3,4]],5] -> [1,2,3,4,5]

2) power(base, exp)
   - base ** exp 를 O(log exp) 로 계산 (분할정복 거듭제곱)
   - exp 는 0 이상의 정수. exp == 0 이면 1
   - 핵심: x^n = (x^(n//2))^2  (n이 홀수면 x를 한 번 더 곱한다)
   - 재귀 호출을 두 번 하면 O(n) 이 되어버린다. 한 번만 호출하고 재사용할 것!

3) hanoi(n, start, mid, end)
   - 원반 n개를 start 에서 end 로 옮기는 이동 순서를 [(from, to), ...] 로 반환
   - 규칙: 한 번에 한 개, 큰 원반을 작은 원반 위에 올릴 수 없음
   - 총 이동 횟수는 2^n - 1

힌트:
- 1) 원소가 리스트면 flatten 결과를 extend, 아니면 append
- 2) half = power(base, exp // 2) 를 변수에 담아두고 재사용
- 3) n-1개를 mid로 -> 가장 큰 원반을 end로 -> n-1개를 mid에서 end로
"""


def flatten(lst):
    # TODO: 각 원소가 리스트인지 isinstance(item, list) 로 확인
    pass


def power(base, exp):
    # TODO: base case (exp == 0)
    # TODO: half 를 한 번만 계산해서 제곱, 홀수면 base 한 번 더
    pass


def hanoi(n, start, mid, end):
    # TODO: base case (n == 0 이면 이동 없음)
    # TODO: n-1개 이동 -> 큰 원반 이동 -> 다시 n-1개 이동
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 중첩 리스트 평탄화 ===")
    for lst in [[1, [2, [3, 4]], 5],
                [[[[1]]]],
                [1, 2, 3],
                [],
                [[], [1, []], 2]]:
        print(f"{lst} -> {flatten(lst)}")
    print()

    print("=== 빠른 거듭제곱 ===")
    for b, e in [(2, 0), (2, 10), (3, 5), (5, 3), (2, 30)]:
        print(f"{b}^{e} = {power(b, e)}")
    print()

    print("=== 하노이의 탑 ===")
    for n in [1, 2, 3]:
        moves = hanoi(n, 'A', 'B', 'C')
        print(f"원반 {n}개: {len(moves)}번 이동 (2^{n}-1 = {2 ** n - 1})")
        for i, (f, t) in enumerate(moves, 1):
            print(f"  {i}. {f} -> {t}")
    print(f"원반 10개 이동 횟수: {len(hanoi(10, 'A', 'B', 'C'))}")
