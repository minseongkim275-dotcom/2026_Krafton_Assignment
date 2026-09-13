#!/bin/bash
# Q2_C_SQ.c (createStackFromLinkedList / removeEvenValues) 자동 테스트
# 사용법: ./q2_test.sh        (Q2_C_SQ.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q2_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q2_C_SQ.c"

# "The resulting stack is: 7 6 5 3 1"
# "The resulting stack after removing even integers is: 7 5 3 1"
PAT_S='s/.*resulting stack is: //p'
PAT_R='s/.*removing even integers is: //p'

bin=$(mktemp /tmp/q2sqtest.XXXXXX) || exit 1
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
    # check "ll에 넣을 값들(순서대로)" "기대 stack(위->아래)" "기대 even 제거 후 stack"
    local a="$1" es="$2" er="$3"
    local inp="" x out gs gr status

    for x in $a; do inp+="1\n$x\n"; done
    inp+="2\n3\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    gs=$(printf '%s\n' "$out" | sed -n "$PAT_S" | tail -1 | sed 's/[[:space:]]*$//')
    gr=$(printf '%s\n' "$out" | sed -n "$PAT_R" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$gs" = "$es" ] && [ "$gr" = "$er" ]; then
        pass=$((pass + 1))
        printf '  OK    ll=[%s]\n' "$a"
    else
        fail=$((fail + 1))
        printf '  FAIL  ll=[%s]\n' "$a"
        printf '          나온것: stack=[%s] even제거후=[%s]\n' "$gs" "$gr"
        printf '          기대값: stack=[%s] even제거후=[%s]\n' "$es" "$er"

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
check "1 3 5 6 7"       "7 6 5 3 1"       "7 5 3 1"
check "2 4 6 8"         "8 6 4 2"         "$E"
check "1 3 5"           "5 3 1"           "5 3 1"
check "10 15 20 25 30"  "30 25 20 15 10"  "25 15"
check ""                "$E"              "$E"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
