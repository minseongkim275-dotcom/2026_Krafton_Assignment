#!/bin/bash
# Q2_A_LL.c (alternateMergeLL) 자동 테스트
# 사용법: ./q2_test.sh        (Q2_A_LL.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q2_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q2_A_LL.c"

# 출력에서 리스트를 뽑아내는 패턴.
# 프로그램 출력이 "Linked list 1: 1 4 2 5" 형태라고 가정합니다.
# 문구가 다르면 아래 두 줄만 고치세요.
PAT1='s/.*[Ll]ist 1: //p'
PAT2='s/.*[Ll]ist 2: //p'

bin=$(mktemp /tmp/q2test.XXXXXX) || exit 1
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
    # check "ll1값들" "ll2값들" "기대ll1" "기대ll2"
    local a="$1" b="$2" e1="$3" e2="$4"
    local inp="" x out g1 g2 status

    for x in $a; do inp+="1\n$x\n"; done
    for x in $b; do inp+="2\n$x\n"; done
    inp+="3\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g1=$(printf '%s\n' "$out" | sed -n "$PAT1" | tail -1 | sed 's/[[:space:]]*$//')
    g2=$(printf '%s\n' "$out" | sed -n "$PAT2" | tail -1 | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$g1" = "$e1" ] && [ "$g2" = "$e2" ]; then
        pass=$((pass + 1))
        printf '  OK    ll1=[%s] ll2=[%s]\n' "$a" "$b"
    else
        fail=$((fail + 1))
        printf '  FAIL  ll1=[%s] ll2=[%s]\n' "$a" "$b"
        printf '          나온것: [%s] / [%s]\n' "$g1" "$g2"
        printf '          기대값: [%s] / [%s]\n' "$e1" "$e2"

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
check "1 2 3"        "4 5 6 7"   "1 4 2 5 3 6"           "7"
check "1 5 7 3 9 11" "6 10 2 4"  "1 6 5 10 7 2 3 4 9 11" "$E"
check "1 2 3 4"      "5 6 7 8"   "1 5 2 6 3 7 4 8"       "$E"
check "1 2"          "3 4 5 6 7" "1 3 2 4"               "5 6 7"
check "1 2 3 4 5"    "6 7"       "1 6 2 7 3 4 5"         "$E"
check ""             "1 2 3"     "$E"                    "1 2 3"
check "1"            "2 3"       "1 2"                   "3"
check "1 2 3"        ""          "1 2 3"                 "$E"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
