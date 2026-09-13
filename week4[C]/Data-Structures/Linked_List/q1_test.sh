#!/bin/bash
# Q1_A_LL.c (insertSortedLL) 자동 테스트
# 사용법: ./q1_test.sh        (Q1_A_LL.c 와 같은 폴더에 두고 실행)
#         DEBUG=1 ./q1_test.sh   (실패 시 프로그램 원본 출력까지 보기)

set -u
cd "$(dirname "$0")" || exit 1

SRC="Q1_A_LL.c"

# 출력에서 값을 뽑아내는 패턴.
# "The resulting sorted linked list is: 2 3 5" / "... was added at index 4" 형태라고 가정합니다.
PAT_LIST='s/.*sorted linked list is: //p'
PAT_IDX='s/.*was added at index //p'

bin=$(mktemp /tmp/q1test.XXXXXX) || exit 1
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
    # check "삽입값들" "기대 정렬 리스트" "기대 index들(삽입 순서와 같은 개수)"
    local vals="$1" e_list="$2" e_idx="$3"
    local inp="" v out g_list g_idx status

    for v in $vals; do inp+="1\n$v\n2\n"; done
    inp+="3\n0\n"

    out=$(printf '%b' "$inp" | timeout 5 "$bin" 2>&1)
    status=$?

    g_list=$(printf '%s\n' "$out" | sed -n "$PAT_LIST" | tail -1 | sed 's/[[:space:]]*$//')
    g_idx=$(printf '%s\n' "$out" | sed -n "$PAT_IDX" | tr '\n' ' ' | sed 's/[[:space:]]*$//')
    e_idx=$(printf '%s' "$e_idx" | sed 's/[[:space:]]*$//')

    if [ "$status" -eq 0 ] && [ "$g_list" = "$e_list" ] && [ "$g_idx" = "$e_idx" ]; then
        pass=$((pass + 1))
        printf '  OK    insert=[%s]\n' "$vals"
    else
        fail=$((fail + 1))
        printf '  FAIL  insert=[%s]\n' "$vals"
        printf '          나온것: list=[%s] idx=[%s]\n' "$g_list" "$g_idx"
        printf '          기대값: list=[%s] idx=[%s]\n' "$e_list" "$e_idx"

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
check "2 3 5 7 9 8"    "2 3 5 7 8 9" "0 1 2 3 4 4"
check "5 7 9 11 15 7"  "5 7 9 11 15" "0 1 2 3 4 -1"
check "10"             "10"          "0"
check "3 3 3"          "3"           "0 -1 -1"
check "5 3 1 4 2"      "1 2 3 4 5"   "0 0 0 2 1"

echo
echo "  통과 $pass / 실패 $fail"
echo
[ "$fail" -eq 0 ]
