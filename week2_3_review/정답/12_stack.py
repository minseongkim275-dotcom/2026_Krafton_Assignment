"""
[복습 12 - 스택]  (Week2 / 12_stack)

핵심 개념:
- LIFO (Last In First Out). 파이썬은 list 의 append/pop 으로 O(1).
- "가장 최근 것부터 처리해야 한다"면 스택이다.
  괄호 짝 맞추기, 수식 계산, 되돌리기(undo), 재귀의 내부 동작 등.
- pop 하기 전에 항상 비어있는지 확인해야 한다. (if stack)
- 모노토닉 스택: 스택 안의 값을 항상 증가/감소 상태로 유지하면
  '오른쪽에서 처음 나오는 더 큰 수' 같은 문제를 O(n) 에 푼다.

문제:
1) is_balanced(s)
   - (), [], {} 세 종류 괄호의 짝이 맞는지 True/False
   - 괄호가 아닌 문자는 무시한다
   - "{[()]}" -> True / "([)]" -> False / "(" -> False

2) eval_postfix(tokens)
   - 후위 표기식(reverse polish)을 계산해서 정수로 반환
   - 연산자는 +, -, *, / 네 가지. 나눗셈은 0 방향 절삭 int(a / b)
   - ["2","3","+","4","*"] -> 20   ((2+3)*4)

3) next_greater(nums)
   - 각 원소마다 '자기 오른쪽에서 처음으로 나오는 더 큰 수'를 담은 리스트
   - 없으면 -1. O(n) (모노토닉 스택)
   - [2,1,2,4,3] -> [4,2,4,-1,-1]

힌트:
- 1) 여는 괄호는 push, 닫는 괄호는 pop 해서 짝이 맞는지 확인. 끝나고 스택은 비어야 한다
- 2) 피연산자는 push, 연산자를 만나면 두 개 pop. 순서 주의! (뒤에 뺀 게 앞 피연산자)
- 3) 스택에는 '아직 답을 못 찾은 인덱스'를 넣어둔다.
     현재 값이 스택 top 의 값보다 크면 그게 답이다
"""

def is_balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token in ('+', '-', '*', '/'):
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack.pop()


def next_greater(nums):
    out = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            out[stack.pop()] = x
        stack.append(i)
    return out


if __name__ == "__main__":
    print("=== 괄호 검사 ===")
    for s in ["{[()]}", "()[]{}", "([)]", "(", ")", "", "a(b[c]d)e", "(()"]:
        print(f"{s!r} -> {is_balanced(s)}")
    print()

    print("=== 후위 표기식 계산 ===")
    for tokens in [["2", "3", "+", "4", "*"],
                   ["5", "1", "2", "+", "4", "*", "+", "3", "-"],
                   ["7", "2", "/"],
                   ["-7", "2", "/"],
                   ["42"]]:
        print(f"{' '.join(tokens)} = {eval_postfix(tokens)}")
    print()

    print("=== 오른쪽에서 처음 나오는 더 큰 수 ===")
    for nums in [[2, 1, 2, 4, 3],
                 [1, 2, 3, 4],
                 [4, 3, 2, 1],
                 [5, 5, 5],
                 [9],
                 []]:
        print(f"{nums} -> {next_greater(nums)}")
