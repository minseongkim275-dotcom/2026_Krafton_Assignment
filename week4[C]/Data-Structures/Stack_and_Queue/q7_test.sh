#!/bin/bash
# Q7_C_SQ.c (balanced) 자동 테스트
# 사용법: ./q7_test.sh        (Q7_C_SQ.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q7_test.sh   (실패 시 프로그램 원본 출력까지 보기)
#
# 주의: 원본 소스의 main()은 balanced()의 참/거짓 출력이 뒤바뀌어 있습니다.
#   if (balanced(str)) printf("not balanced!\n"); else printf("balanced!\n");
# 즉, 화면에 "balanced!"가 찍히려면 balanced()가 0을 반환해야 합니다.
# 이 테스트는 실제로 화면에 찍히는 문구를 기준으로 채점합니다.

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q7_C_SQ.c"

# 참고: scanf 프롬프트 뒤에 개행 없이 바로 출력되므로 줄 단위가 아니라
# 문자열 자체를 찾아서 비교합니다("not balanced!"가 "balanced!"를 포함하므로 grep -E 사용).

bin=$(mktemp /tmp/q7sqtest.XXXXXX) || exit 1
trap 'rm -f "$bin"' EXIT

if [ ! -f "$SRC" ]; then
    echo "$SRC 를 찾을 수 없습니다. 스크립트를 소스와 같은 폴더에 두세요."
    exit 1
fi

if ! gcc -g -Wall -Wextra -std=c11 "$SRC" -o "$bin"; then
    echo "컴파일 실패"
    exit 1
fi

pass=0
fail=0

check() {
    # check "표현식(공백없이)" "기대(balanced/not)"
    local expr="$1" expect="$2"
    local inp out g status e_text

    inp="1\n$expr\n2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g=$(printf '%s\n' "$out" | grep -oE 'not balanced!|balanced!' | tail -1)

    if [ "$expect" = "yes" ]; then
        e_text="balanced!"
    else
        e_text="not balanced!"
    fi

    if [ "$status" -eq 0 ] && [ "$g" = "$e_text" ]; then
        pass=$((pass + 1))
        printf '  OK    expr=[%s]\n' "$expr"
    else
        fail=$((fail + 1))
        printf '  FAIL  expr=[%s]\n' "$expr"
        printf '          나온것: [%s]\n' "$g"
        printf '          기대값: [%s]\n' "$e_text"

        if [ "$status" -eq 124 ]; then
            printf '          무한 루프 의심 (5초 초과)\n'
        elif [ "$status" -ne 0 ]; then
            printf '          비정상 종료: %s\n' "$status"
        fi

        if [ "${DEBUG:-0}" != "0" ]; then
            printf '          ----- 원본 출력 -----\n'
            printf '%s\n' "$out" | sed 's/^/          /'
            printf '          ---------------------\n'
        fi
    fi
}

echo
check "()"           "yes"
check "([])"         "yes"
check "{[]()[]}"     "yes"
check "{{)]"         "no"
check "[({{)])"      "no"
check "(("            "no"
check ")("            "no"
check "([)]"          "no"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
