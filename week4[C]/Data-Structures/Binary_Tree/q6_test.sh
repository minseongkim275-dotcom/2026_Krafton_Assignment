#!/bin/bash
# Q6_E_BT.c (printSmallerValues) 자동 테스트
# 사용법: ./q6_test.sh        (Q6_E_BT.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q6_test.sh   (실패 시 프로그램 원본 출력까지 보기)
#
# 트리 입력 순서: root 값 -> 스택에서 꺼낸 노드마다 (왼쪽, 오른쪽) 순서로 입력.
# 자식이 없으면 a. createTree()가 right를 먼저 push 하므로 left부터 처리됩니다.

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q6_E_BT.c"
PAT='s/.*The values smaller than [0-9-]* are: //p'

bin=$(mktemp /tmp/q6bt.XXXXXX) || exit 1
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
    # check "설명" "트리 입력 시퀀스" "기준값 m" "기대 출력"
    local desc="$1" seq="$2" m="$3" e="$4"
    local inp="1\n" x out g status

    for x in $seq; do inp+="$x\n"; done
    inp+="2\n$m\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?
    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1 \
        | sed 's/Please input your choice.*//' | sed 's/[[:space:]]*$//')
    report "$desc" "$g" "$e" "$status" "$out"
}

echo
check "PDF 예시 m=55" "50 30 60 25 65 a a a a 10 75 a a a a" "55" "50 30 25 10"
check "전부 포함 m=100" "50 30 60 25 65 a a a a 10 75 a a a a" "100" "50 30 25 65 60 10 75"
check "하나도 없음 m=10" "50 30 60 25 65 a a a a 10 75 a a a a" "10" ""
check "bal7 m=5" "4 2 6 1 3 a a a a 5 7 a a a a" "5" "4 2 1 3"
check "경계값 m=42 (자기 자신 제외)" "42 a a" "42" ""
check "단일 노드 m=50" "42 a a" "50" "42"
check "빈 트리" "a" "50" ""

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
