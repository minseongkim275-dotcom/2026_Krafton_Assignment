#!/bin/bash
# Q3_C_SQ.c (isStackPairwiseConsecutive) 자동 테스트
# 사용법: ./q3_test.sh        (Q3_C_SQ.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q3_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q3_C_SQ.c"

# "The stack is pairwise consecutive." / "The stack is not pairwise consecutive."
PAT='s/.*\(The stack is\( not\)\? pairwise consecutive\)\.$/\1/p'

bin=$(mktemp /tmp/q3sqtest.XXXXXX) || exit 1
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
    # check "스택 top->bottom 순서로 넣을 값들" "기대 결과(yes/no)"
    local topToBottom="$1" expect="$2"
    local rev="" x out g status e_text

    # push는 항상 맨 앞에 쌓이므로, top->bottom 순서를 만들려면 반대 순서로 push해야 함
    for x in $topToBottom; do rev="$x $rev"; done

    local inp=""
    for x in $rev; do inp+="1\n$x\n"; done
    inp+="2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1)

    if [ "$expect" = "yes" ]; then
        e_text="The stack is pairwise consecutive"
    else
        e_text="The stack is not pairwise consecutive"
    fi

    if [ "$status" -eq 0 ] && [ "$g" = "$e_text" ]; then
        pass=$((pass + 1))
        printf '  OK    stack(top->bottom)=[%s]\n' "$topToBottom"
    else
        fail=$((fail + 1))
        printf '  FAIL  stack(top->bottom)=[%s]\n' "$topToBottom"
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
check "16 15 11 10 5 4"  "yes"
check "16 15 11 10 5 1"  "no"
check "16 15 11 10 5"    "no"
check "3 2 9 8"          "yes"
check "1 2 3 4"          "yes"
check "5 3 8 8"          "no"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
