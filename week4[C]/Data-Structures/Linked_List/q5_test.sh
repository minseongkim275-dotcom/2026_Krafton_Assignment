#!/bin/bash
# Q5_A_LL.c (frontBackSplitLinkedList) 자동 테스트
# 사용법: ./q5_test.sh        (Q5_A_LL.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q5_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q5_A_LL.c"

# "Front linked list: 2 3 5" / "Back linked list: 6 7"
PAT_FRONT='s/.*Front linked list: //p'
PAT_BACK='s/.*Back linked list: //p'

bin=$(mktemp /tmp/q5test.XXXXXX) || exit 1
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
    # check "입력값들" "기대 front" "기대 back"
    local a="$1" ef="$2" eb="$3"
    local inp="" x out gf gb status

    for x in $a; do inp+="1\n$x\n"; done
    inp+="2\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    gf=$(printf '%s\n' "$out" | sed -n "$PAT_FRONT" | tail -1 | sed 's/[[:space:]]*$//')
    gb=$(printf '%s\n' "$out" | sed -n "$PAT_BACK" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$gf" = "$ef" ] && [ "$gb" = "$eb" ]; then
        pass=$((pass + 1))
        printf '  OK    ll=[%s]\n' "$a"
    else
        fail=$((fail + 1))
        printf '  FAIL  ll=[%s]\n' "$a"
        printf '          나온것: front=[%s] back=[%s]\n' "$gf" "$gb"
        printf '          기대값: front=[%s] back=[%s]\n' "$ef" "$eb"

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
check "2 3 5 6 7"     "2 3 5"   "6 7"
check "1 2 3 4"       "1 2"     "3 4"
check "1 2 3 4 5 6"   "1 2 3"   "4 5 6"
check "5"             "5"       "$E"
check ""              "$E"      "$E"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
