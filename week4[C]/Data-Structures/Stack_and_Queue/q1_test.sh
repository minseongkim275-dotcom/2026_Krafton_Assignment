#!/bin/bash
# Q1_C_SQ.c (createQueueFromLinkedList / removeOddValues) 자동 테스트
# 사용법: ./q1_test.sh        (Q1_C_SQ.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q1_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q1_C_SQ.c"

# "The resulting queue is: 1 2 3 4 5"
# "The resulting queue after removing odd integers is: 2 4 6"
PAT_Q='s/.*resulting queue is: //p'
PAT_R='s/.*removing odd integers is: //p'

bin=$(mktemp /tmp/q1sqtest.XXXXXX) || exit 1
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
    # check "ll에 넣을 값들" "기대 queue" "기대 odd 제거 후 queue"
    local a="$1" eq="$2" er="$3"
    local inp="" x out gq gr status

    for x in $a; do inp+="1\n$x\n"; done
    inp+="2\n3\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    gq=$(printf '%s\n' "$out" | sed -n "$PAT_Q" | tail -1 | sed 's/[[:space:]]*$//')
    gr=$(printf '%s\n' "$out" | sed -n "$PAT_R" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$gq" = "$eq" ] && [ "$gr" = "$er" ]; then
        pass=$((pass + 1))
        printf '  OK    ll=[%s]\n' "$a"
    else
        fail=$((fail + 1))
        printf '  FAIL  ll=[%s]\n' "$a"
        printf '          나온것: queue=[%s] odd제거후=[%s]\n' "$gq" "$gr"
        printf '          기대값: queue=[%s] odd제거후=[%s]\n' "$eq" "$er"

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

E="Empty"

echo
check "1 2 3 4 5 6 7" "1 2 3 4 5 6 7" "2 4 6"
check "2 4 6"         "2 4 6"         "2 4 6"
check "1 3 5"         "1 3 5"         "$E"
check "10 15 20 25 30" "10 15 20 25 30" "10 20 30"
check ""              "$E"            "$E"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
