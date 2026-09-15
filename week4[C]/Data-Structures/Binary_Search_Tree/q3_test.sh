#!/bin/bash
# Q3_F_BST.c (preOrderIterative) 자동 테스트
# 사용법: ./q3_test.sh        (Q3_F_BST.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q3_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q3_F_BST.c"

# "The resulting pre-order traversal of the binary search tree is: 20 15 50"
PAT='s/.*binary search tree is: //p'

bin=$(mktemp /tmp/q3bst.XXXXXX) || exit 1
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
    # check "삽입할 값들(공백구분)" "기대 출력"
    local vals="$1" e="$2"
    local inp="" v out g status

    for v in $vals; do inp+="1\n$v\n"; done
    inp+="2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$g" = "$e" ]; then
        pass=$((pass + 1))
        printf '  OK    삽입=[%s]\n' "$vals"
    else
        fail=$((fail + 1))
        printf '  FAIL  삽입=[%s]\n' "$vals"
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

echo
check "20 15 50 10 18 25 80"    "20 15 10 18 50 25 80"
check "50 30 70 20 40 60 80"    "50 30 20 40 70 60 80"
check "8 3 10 1 6 14 4 7 13"    "8 3 1 6 4 7 10 14 13"
check "1 2 3 4 5"               "1 2 3 4 5"
check "5 4 3 2 1"               "5 4 3 2 1"
check "42"                      "42"
check ""                        ""

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
