"""
[복습 07 - 시간복잡도]  (Week2 / 07_complexity)

핵심 개념:
- 빅오는 '입력이 커질 때 연산 횟수가 어떤 비율로 늘어나는가'만 본다.
  상수배와 낮은 차수는 버린다.  3n^2 + 100n + 7  ->  O(n^2)
- 반복문이 중첩되면 곱하기, 나란히 있으면 더하기(=큰 쪽만 남는다).
- 반복마다 크기가 절반이 되면 O(log n).
- 자주 나오는 순서 (작을수록 빠름):
  O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)

문제:
1) count_ops_pairs(n)
   - 아래 코드의 print 실행 횟수를 '반복문 없이 수식으로' 반환
       for i in range(n):
           for j in range(i + 1, n):
               print(i, j)
   - n=5 -> 10  (= n(n-1)/2). n <= 1 이면 0

2) count_ops_halving(n)
   - 아래 코드의 반복 횟수를 반환 (n >= 1)
       while n > 1:
           n //= 2
   - n=8 -> 3, n=10 -> 3, n=1 -> 0  (= floor(log2 n))

3) big_o(algorithm)
   - 알고리즘 이름을 받아 시간복잡도 문자열을 반환. 목록에 없으면 "모름"
   - 표기는 "O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)", "O(n!)"

     "배열 인덱스 접근"        -> O(1)
     "해시 테이블 평균 조회"    -> O(1)
     "이진 탐색"              -> O(log n)
     "선형 탐색"              -> O(n)
     "병합 정렬"              -> O(n log n)
     "퀵 정렬 평균"           -> O(n log n)
     "버블 정렬"              -> O(n^2)
     "삽입 정렬 최악"          -> O(n^2)
     "모든 부분집합 완전탐색"   -> O(2^n)
     "모든 순열 완전탐색"      -> O(n!)

힌트:
- 1) i=0일 때 n-1번, i=1일 때 n-2번, ... 등차수열의 합
- 2) 반복문으로 세도 되지만 while 한 줄이면 충분하다
- 3) 딕셔너리 하나면 끝. .get(키, "모름")
"""

def count_ops_pairs(n):
    if n <= 1:
        return 0
    return n * (n - 1) // 2


def count_ops_halving(n):
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count


def big_o(algorithm):
    table = {
        "배열 인덱스 접근": "O(1)",
        "해시 테이블 평균 조회": "O(1)",
        "이진 탐색": "O(log n)",
        "선형 탐색": "O(n)",
        "병합 정렬": "O(n log n)",
        "퀵 정렬 평균": "O(n log n)",
        "버블 정렬": "O(n^2)",
        "삽입 정렬 최악": "O(n^2)",
        "모든 부분집합 완전탐색": "O(2^n)",
        "모든 순열 완전탐색": "O(n!)",
    }
    return table.get(algorithm, "모름")


if __name__ == "__main__":
    print("=== 이중 반복문 실행 횟수 ===")
    for n in [0, 1, 2, 5, 10, 100, 1000]:
        print(f"n={n} -> {count_ops_pairs(n)}")
    print()

    # 실제로 세어본 값과 같은지 검증
    print("=== 공식 검증 (실제로 세어본 값과 비교) ===")
    for n in [0, 1, 5, 10, 30]:
        actual = 0
        for i in range(n):
            for j in range(i + 1, n):
                actual += 1
        print(f"n={n}: 공식={count_ops_pairs(n)}, 실제={actual}, 일치={count_ops_pairs(n) == actual}")
    print()

    print("=== 절반씩 줄이기 반복 횟수 ===")
    for n in [1, 2, 3, 8, 10, 1024, 1000000]:
        print(f"n={n} -> {count_ops_halving(n)}")
    print()

    print("=== 시간복잡도 퀴즈 ===")
    for name in ["배열 인덱스 접근", "해시 테이블 평균 조회", "이진 탐색", "선형 탐색",
                 "병합 정렬", "퀵 정렬 평균", "버블 정렬", "삽입 정렬 최악",
                 "모든 부분집합 완전탐색", "모든 순열 완전탐색", "듣도 보도 못한 정렬"]:
        print(f"{name}: {big_o(name)}")
