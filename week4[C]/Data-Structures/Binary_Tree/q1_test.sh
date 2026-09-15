#!/bin/bash
# Q1_E_BT.c (identical) 자동 테스트
# 사용법: ./q1_test.sh        (Q1_E_BT.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q1_test.sh   (실패 시 프로그램 원본 출력까지 보기)
#
# 트리 입력 순서: root 값 -> 스택에서 꺼낸 노드마다 (왼쪽, 오른쪽) 순서로 입력.
# 자식이 없으면 a. createTree()가 right를 먼저 push 하므로 left부터 처리됩니다.

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q1_E_BT.c"
PAT='s/.*\(Both trees are [a-z ]*\.\)$/\1/p'

bin=$(mktemp /tmp/q1bt.XXXXXX) || exit 1
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
    # check "설명" "tree1 시퀀스" "tree2 시퀀스" "기대 출력"
    local desc="$1" s1="$2" s2="$3" e="$4"
    local inp="1\n" x out g status

    for x in $s1; do inp+="$x\n"; done
    inp+="2\n"
    for x in $s2; do inp+="$x\n"; done
    inp+="3\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?
    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1 | sed 's/[[:space:]]*$//')
    report "$desc" "$g" "$e" "$status" "$out"
}

echo
check "같은 트리 full7 vs full7" "5 3 7 1 2 a a a a 4 8 a a a a" "5 3 7 1 2 a a a a 4 8 a a a a" "Both trees are structurally identical."
check "값 다름 full7 vs bal7" "5 3 7 1 2 a a a a 4 8 a a a a" "4 2 6 1 3 a a a a 5 7 a a a a" "Both trees are different."
check "구조 다름 full7 vs mirror" "5 3 7 1 2 a a a a 4 8 a a a a" "4 5 2 a 6 a a 3 1 a a a a" "Both trees are different."
check "한쪽만 비어있음" "5 3 7 1 2 a a a a 4 8 a a a a" "a" "Both trees are different."
check "둘 다 비어있음" "a" "a" "Both trees are structurally identical."
check "단일 노드 같음" "42 a a" "42 a a" "Both trees are structurally identical."
check "단일 vs 두 노드" "42 a a" "10 5 a a a" "Both trees are different."

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
