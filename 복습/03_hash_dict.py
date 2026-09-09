"""
[복습 03 - 딕셔너리/집합 활용]  (Week2 / 03_python_dict, 15_hash_table)

핵심 개념:
- dict/set 의 조회·삽입은 평균 O(1). "찾아본 적 있나?"를 기억하는 도구.
- 리스트로 in 검사를 하면 O(n) -> 반복문 안에서 쓰면 O(n^2)가 된다.
- '무엇을 key 로 삼을지' 정하는 게 해시 문제의 핵심.
  (애너그램이면 정렬한 문자열, 좌표면 튜플, ...)

문제:
1) two_sum(nums, target)
   - 두 원소의 합이 target 이 되는 인덱스 쌍 (i, j) 를 i < j 로 반환
   - 없으면 None. 여러 개면 j 가 가장 작은 것. 반드시 O(n) 으로!
   - [2,7,11,15], 9 -> (0, 1)

2) group_anagrams(words)
   - 애너그램(글자 구성이 같은 단어)끼리 묶는다
   - 각 그룹은 사전순 정렬, 그룹들도 사전순 정렬해서 반환
   - ["eat","tea","tan","ate","nat","bat"]
     -> [['ate','eat','tea'], ['bat'], ['nat','tan']]

3) top_k_frequent(nums, k)
   - 가장 많이 등장한 값 k개를 빈도 내림차순으로 반환
   - 빈도가 같으면 값이 작은 순
   - [1,1,1,2,2,3], 2 -> [1, 2]

힌트:
- 1) "target - x 를 전에 본 적 있나?" 를 dict 에 기록하며 한 번만 훑는다
- 2) key = ''.join(sorted(word))
- 3) sorted(..., key=lambda kv: (-kv[1], kv[0]))
"""


def two_sum(nums, target):
    # TODO: {값: 인덱스} 딕셔너리를 만들면서 한 번 훑기
    pass


def group_anagrams(words):
    # TODO: 정렬한 문자열을 key 로 묶고, 정렬해서 반환
    pass


def top_k_frequent(nums, k):
    # TODO: 빈도를 세고, (-빈도, 값) 기준으로 정렬해서 앞 k개
    pass


# 테스트 케이스
if __name__ == "__main__":
    print("=== 두 수의 합 ===")
    for nums, target in [([2, 7, 11, 15], 9),
                         ([3, 2, 4], 6),
                         ([3, 3], 6),
                         ([1, 2, 3], 100)]:
        print(f"{nums}, target={target} -> {two_sum(nums, target)}")
    print()

    print("=== 애너그램 그룹 ===")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"입력: {words}")
    for group in group_anagrams(words):
        print(f"  {group}")
    print(f"빈 입력 -> {group_anagrams([])}")
    print()

    print("=== 빈도 상위 k개 ===")
    for nums, k in [([1, 1, 1, 2, 2, 3], 2),
                    ([1], 1),
                    ([4, 4, 3, 3, 2], 3),
                    ([5, 6, 7], 2)]:
        print(f"{nums}, k={k} -> {top_k_frequent(nums, k)}")
