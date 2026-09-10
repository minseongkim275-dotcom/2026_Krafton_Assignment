#!/usr/bin/env python3
"""
복습 문제 채점 스크립트

사용법:
  python check.py                  # 전체 채점
  python check.py --all            # 전체 채점 (위와 동일)
  python check.py 01               # 01번 문제만 채점
  python check.py 01_string.py     # 파일명으로 채점
  python check.py --list           # 문제 목록 보기
  python check.py --diff 01        # 01번 채점 + 틀린 줄 전부 보기

채점 방식:
  문제 파일을 실행한 표준 출력을 NN_xxx_output.txt 와 줄 단위로 비교합니다.
  (앞뒤 공백과 빈 줄은 무시)
"""

import re
import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TIMEOUT = 30
PATTERN = re.compile(r"^(\d{2})_.+\.py$")


def discover_problem_files():
    files = []
    for entry in SCRIPT_DIR.iterdir():
        if entry.is_file() and entry.name != "check.py":
            m = PATTERN.match(entry.name)
            if m:
                files.append((int(m.group(1)), entry.name))
    files.sort()
    return [name for _, name in files]


def resolve(arg):
    """'01', '01_string', '01_string.py' 를 실제 파일명으로"""
    candidates = discover_problem_files()
    arg = arg.strip()
    if arg in candidates:
        return arg
    if arg + ".py" in candidates:
        return arg + ".py"
    matches = [n for n in candidates if n.startswith(arg)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"'{arg}' 로 시작하는 문제가 여러 개입니다: {', '.join(matches)}")
    return None


def normalize(text):
    return [line.rstrip() for line in text.strip().split("\n") if line.strip()]


def run_problem(problem_file):
    """(성공여부, 실제출력줄, 기대출력줄, 에러메시지)"""
    problem_path = SCRIPT_DIR / problem_file
    output_path = SCRIPT_DIR / (problem_file[:-3] + "_output.txt")

    if not problem_path.exists():
        return False, [], [], f"파일이 없습니다: {problem_file}"
    if not output_path.exists():
        return False, [], [], f"정답 출력 파일이 없습니다: {output_path.name}"

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, str(problem_path)],
            capture_output=True, text=True, encoding="utf-8",
            timeout=TIMEOUT, cwd=str(SCRIPT_DIR), env=env,
        )
    except subprocess.TimeoutExpired:
        return False, [], [], f"시간 초과 ({TIMEOUT}초). 무한 루프나 비효율적인 풀이일 수 있습니다."

    expected = normalize(output_path.read_text(encoding="utf-8"))

    if result.returncode != 0:
        err = (result.stderr or "").strip().split("\n")
        tail = "\n     ".join(err[-4:])
        return False, [], expected, f"실행 중 오류가 발생했습니다.\n     {tail}"

    actual = normalize(result.stdout)
    return actual == expected, actual, expected, None


def first_mismatch(actual, expected):
    for i in range(max(len(actual), len(expected))):
        a = actual[i] if i < len(actual) else None
        e = expected[i] if i < len(expected) else None
        if a != e:
            return i, a, e
    return None


def report_diff(actual, expected, show_all):
    mismatch = first_mismatch(actual, expected)
    if mismatch is None:
        return
    i, a, e = mismatch
    print(f"     출력 줄 수: 기대 {len(expected)}줄 / 실제 {len(actual)}줄")
    print(f"     처음 틀린 곳: {i + 1}번째 줄")
    print(f"       기대: {e if e is not None else '(줄 없음 - 출력이 부족합니다)'}")
    print(f"       실제: {a if a is not None else '(줄 없음 - 출력이 부족합니다)'}")

    if not show_all:
        return
    print("     --- 틀린 줄 전체 ---")
    for j in range(max(len(actual), len(expected))):
        a = actual[j] if j < len(actual) else None
        e = expected[j] if j < len(expected) else None
        if a != e:
            print(f"     {j + 1:>3} 기대: {e}")
            print(f"         실제: {a}")


def check_one(problem_file, show_all=False, verbose=True):
    passed, actual, expected, error = run_problem(problem_file)
    if verbose:
        if passed:
            print(f"  [PASS] {problem_file}")
        elif error:
            print(f"  [FAIL] {problem_file}")
            print(f"     {error}")
        else:
            print(f"  [FAIL] {problem_file}")
            report_diff(actual, expected, show_all)
    return passed


def topic_of(problem_file):
    """문제 파일의 docstring 첫 줄에서 제목을 뽑아온다"""
    try:
        text = (SCRIPT_DIR / problem_file).read_text(encoding="utf-8")
        m = re.search(r"^\[(.+?)\]", text, re.M)
        if m:
            return m.group(1)
    except OSError:
        pass
    return ""


def run_all(show_all=False):
    problems = discover_problem_files()
    if not problems:
        print("채점할 문제 파일이 없습니다.")
        return 1

    print("=" * 64)
    print(f"복습 문제 전체 채점 (총 {len(problems)}개)")
    print("=" * 64)

    failed = []
    for name in problems:
        if not check_one(name, show_all=show_all):
            failed.append(name)

    print("=" * 64)
    passed = len(problems) - len(failed)
    print(f"결과: {passed} / {len(problems)} 통과")
    if failed:
        print("아직 못 푼 문제:")
        for name in failed:
            print(f"  - {name}  {topic_of(name)}")
    else:
        print("전부 통과했습니다!")
    print("=" * 64)
    return 0 if not failed else 1


def run_single(arg, show_all=False):
    name = resolve(arg)
    if name is None:
        print(f"'{arg}' 에 해당하는 문제를 찾을 수 없습니다. python check.py --list 로 확인하세요.")
        return 1

    print("=" * 64)
    print(f"{name}  {topic_of(name)}")
    print("=" * 64)

    passed = check_one(name, show_all=show_all)
    print()
    if passed:
        print("통과! 다음 문제로 넘어가세요.")
        return 0
    print("문제 파일의 TODO 부분을 다시 확인해보세요.")
    print(f"정답 코드는 정답/{name} 에 있습니다. (되도록 먼저 스스로 풀어볼 것)")
    return 1


def list_problems():
    problems = discover_problem_files()
    print(f"복습 문제 {len(problems)}개")
    print("-" * 64)
    for name in problems:
        print(f"  {name:<24} {topic_of(name)}")
    print("-" * 64)
    print("채점: python check.py 01   /   전체: python check.py")


def main():
    args = [a for a in sys.argv[1:]]
    show_all = "--diff" in args
    args = [a for a in args if a != "--diff"]

    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args and args[0] == "--list":
        list_problems()
        return 0
    if not args or args[0] == "--all":
        return run_all(show_all=show_all)
    return run_single(args[0], show_all=show_all)


if __name__ == "__main__":
    sys.exit(main())
