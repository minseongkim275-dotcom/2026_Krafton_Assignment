"""
[복습 01 - 문자열 처리]  (Week2 / 01_string)

핵심 개념:
- 파이썬 문자열은 불변(immutable). 바꾸려면 새로 만들어야 한다.
- 반복문 안에서 s += ch 는 매번 새 문자열을 만들어 O(n^2).
  -> 리스트에 모았다가 ''.join(리스트) 로 O(n).
- 양끝에서 좁혀오는 투 포인터는 문자열 문제의 기본 패턴.

문제:
1) is_palindrome(s)
   - 영문자와 숫자만 보고, 대소문자를 무시하고 팰린드롬인지 판별
   - "A man, a plan, a canal: Panama" -> True / "hello" -> False
   - 빈 문자열은 True

2) compress(s)
   - 연속된 문자를 (문자 + 개수) 로 압축 (Run-Length Encoding)
   - 단, 압축 결과가 원본보다 짧지 않으면 원본을 그대로 반환
   - "aabcccccaaa" -> "a2b1c5a3" / "abc" -> "abc" / "aabb" -> "aabb"

3) reverse_words(s)
   - 단어의 순서를 뒤집는다. 앞뒤/중간의 여분 공백은 하나로 정리
   - "  the sky   is blue  " -> "blue is sky the"

힌트:
- 1) ch.isalnum(), ch.lower()
- 2) 앞 글자와 같은지 비교하며 개수를 세고, 달라지는 순간 기록
- 3) s.split() 은 인자가 없으면 연속 공백을 알아서 무시한다
"""

def is_palindrome(s):
    t = [ch.lower() for ch in s if ch.isalnum()]
    i, j = 0, len(t) - 1
    while i < j:
        if t[i] != t[j]:
            return False
        i += 1
        j -= 1
    return True


def compress(s):
    if not s:
        return s
    parts = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(s[i - 1] + str(count))
            count = 1
    parts.append(s[-1] + str(count))
    compressed = ''.join(parts)
    return compressed if len(compressed) < len(s) else s


def reverse_words(s):
    return ' '.join(reversed(s.split()))


if __name__ == "__main__":
    print("=== 팰린드롬 판별 ===")
    for s in ["A man, a plan, a canal: Panama",
              "racecar",
              "hello",
              "",
              "Was it a car or a cat I saw?",
              "0P"]:
        print(f"{s!r} -> {is_palindrome(s)}")
    print()

    print("=== 문자열 압축 (RLE) ===")
    for s in ["aabcccccaaa", "abc", "aabb", "a", "", "aaabbbcccd"]:
        print(f"{s!r} -> {compress(s)!r}")
    print()

    print("=== 단어 순서 뒤집기 ===")
    for s in ["the sky is blue", "  hello   world  ", "python", "  a  "]:
        print(f"{s!r} -> {reverse_words(s)!r}")
