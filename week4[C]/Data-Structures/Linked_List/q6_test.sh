#!/bin/bash
# Q6_A_LL.c (moveMaxToFront) 자동 테스트
# 사용법: ./q6_test.sh        (Q6_A_LL.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q6_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q6_A_LL.c"

# "The resulting linked list after moving largest stored value to the front of the list is: 70 30 20 40 50"
PAT='s/.*front of the list is: //p'

bin=$(mktemp /tmp/q6test.XXXXXX) || exit 1
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
    # check "입력값들" "기대 결과"
    local a="$1" e="$2"
    local inp="" x out g status

    for x in $a; do inp+="1\n$x\n"; done
    inp+="2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g=$(printf '%s\n' "$out" | sed -n "$PAT" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$g" = "$e" ]; then
        pass=$((pass + 1))
        printf '  OK    ll=[%s]\n' "$a"
    else
        fail=$((fail + 1))
        printf '  FAIL  ll=[%s]\n' "$a"
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
check "30 20 40 70 50" "70 30 20 40 50"
check "1 2 3"          "3 1 2"
check "5"              "5"
check "7 3 9 4 2"      "9 7 3 4 2"
check "10 20 5 3"      "20 10 5 3"
check "-5 -1 -10"      "-1 -5 -10"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
