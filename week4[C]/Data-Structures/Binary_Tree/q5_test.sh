#!/bin/bash
# Q5_E_BT.c (mirrorTree) 자동 테스트
# 사용법: ./q5_test.sh        (Q5_E_BT.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q5_test.sh   (실패 시 프로그램 원본 출력까지 보기)
#
# 트리 입력 순서: root 값 -> 스택에서 꺼낸 노드마다 (왼쪽, 오른쪽) 순서로 입력.
# 자식이 없으면 a. createTree()가 right를 먼저 push 하므로 left부터 처리됩니다.

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q5_E_BT.c"
PAT='s/.*Mirror binary tree is: //p'

bin=$(mktemp /tmp/q5bt.XXXXXX) || exit 1
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

report() {
    local desc="$1" g="$2" e="$3" status="$4" out="$5"
    if [ "$status" -eq 0 ] && [ "$g" = "$e" ]; then
        pass=$((pass + 1))
        printf '  OK    %s\n' "$desc"
    else
        fail=$((fail + 1))
        printf '  FAIL  %s\n' "$desc"
        printf '          나온것: [%s]\n' "$g"
        printf '          기대값: [%s]\n' "$e"
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

check() {
    # check "설명" "트리 입력 시퀀스" "기대 출력"
    local desc="$1" seq="$2" e="$3"
    local inp="1\n" x out g status

    for x in $seq; do inp+="$x\n"; done
    inp+="2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?
    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1 \
        | sed 's/Please input your choice.*//' | sed 's/[[:space:]]*$//')
    report "$desc" "$g" "$e" "$status" "$out"
}

echo
check "PDF 예시" "4 5 2 a 6 a a 3 1 a a a a" "1 2 3 4 6 5"
check "full7" "5 3 7 1 2 a a a a 4 8 a a a a" "8 7 4 5 2 3 1"
check "bal7" "4 2 6 1 3 a a a a 5 7 a a a a" "7 6 5 4 3 2 1"
check "왼쪽 사슬" "1 2 a 3 a a a" "1 2 3"
check "노드 2개" "10 5 a a a" "10 5"
check "단일 노드" "42 a a" "42"
check "빈 트리" "a" ""

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
