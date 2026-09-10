# 🏕️ 2026 Krafton Jungle — SW-AI Assignment

> Krafton Jungle **SW-AI: 컴퓨팅 사고로의 전환** 과정에서 진행한 개인 과제/복습 저장소입니다.
> Week 2~3 은 Python, Week 4 는 C로 기초 자료구조·알고리즘을 다시 구현하며 학습했습니다.

<p>
  <img alt="python" src="https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white">
  <img alt="c" src="https://img.shields.io/badge/C-GCC-00599C?logo=c&logoColor=white">
  <img alt="status" src="https://img.shields.io/badge/status-in%20progress-yellow">
</p>

---

## 📂 폴더 구조

```
2026_Krafton_assignment/
├── week2[Python]/
│   ├── 1. basic/             # 기본 개념 학습 (15문제)
│   │   ├── 01_string.py ~ 15_hash_table.py
│   │   └── check.py                 # 자동 탐지 채점기
│   └── 2. advanced/          # 심화 문제 (5문제, 난이도순)
│       ├── 01_quick_sort.py ~ 05_n_queen.py
│       └── check.py
├── week3[Python]/
│   ├── 1. basic/             # 기본 개념 학습 (9문제)
│   │   ├── 01_binary_tree.py ~ 09_greedy_meeting.py
│   │   └── check.py
│   └── 2. advanced/          # 심화 문제 (3문제, 난이도순)
│       ├── 01_topological_sort.py ~ 03_dijkstra.py
│       └── check.py
├── week2_3_review/           # Week2+3 통합 복습 (20문제 + 정답 폴더)
│   ├── 01_string.py ~ 20_advanced.py
│   ├── 정답/                        # 막혔을 때만 열어보는 참고 정답
│   ├── check.py                     # --list / --diff 지원 채점기
│   └── README.md                    # 복습 문제 전용 안내
├── week4[C]/                 # C로 구현하는 기초 자료구조 (총 27문제)
│   ├── Linked_List/                 # Q1~Q7 + 문제지 PDF
│   ├── Stack_and_Queue/             # Q1~Q7 + 문제지 PDF
│   ├── Binary_Tree/                 # Q1~Q8 + 문제지 PDF
│   └── Binary_Search_Tree/          # Q1~Q5 + 문제지 PDF
└── README.md                 # 본 문서
```

> ℹ️ **현재 문제 구성 요약**
> | 폴더 | 언어 | 문제 수 | 비고 |
> |---|---|---|---|
> | `week2[Python]/1. basic` | Python | 15 | 문자열/배열/딕셔너리부터 자료구조까지 |
> | `week2[Python]/2. advanced` | Python | 5 | 분할정복·재귀·백트래킹 응용 |
> | `week3[Python]/1. basic` | Python | 9 | 트리/그래프/DP/그리디 입문 |
> | `week3[Python]/2. advanced` | Python | 3 | 그래프 응용 + 고급 DP |
> | `week2_3_review` | Python | 20 | Week2~3 개념 통합 복습 + 정답 제공 |
> | `week4[C]` | C | 27 | 연결 리스트/스택·큐/이진 트리/BST를 C로 직접 구현 |

---

## ⚙️ 실행 환경 준비

### Python (`week2[Python]`, `week3[Python]`, `week2_3_review`)

외부 라이브러리 없이 **순수 표준 Python** 만으로 풀 수 있습니다. 별도 `pip install` 불필요.

- **Python 3.8 이상** (권장: 최신 3.x)
- 채점기(`check.py`)가 내부적으로 `python3` 명령을 호출하므로, `python` 이 아니라 **`python3`** 명령이 사용 가능해야 합니다. (Windows 는 `python` 또는 `py`)

```bash
# 설치 확인
python3 --version   # macOS / Linux
python --version    # Windows
```

- macOS: `brew install python`
- Windows: [python.org](https://www.python.org/downloads/) 에서 설치 시 **"Add Python to PATH"** 체크
- Linux: `sudo apt install python3`

### C (`week4[C]`)

GCC(또는 다른 C 컴파일러)가 필요합니다.

```bash
# 설치 확인
gcc --version

# 단일 파일 컴파일 & 실행 예시
cd "week4[C]/Linked_List"
gcc Q1_A_LL.c -o q1 && ./q1
```

---

## 📝 문제 풀이 방법

### Python — 자동 채점기 사용법

각 폴더의 `check.py` 는 같은 폴더 안의 `NN_*.py` 파일을 자동으로 찾아 채점합니다.
번호가 늘어나거나 줄어들어도 스크립트를 수정할 필요 없이 그대로 사용할 수 있습니다.

```bash
# Week2 기본 문제 전체 (01~15) 채점
cd "week2[Python]/1. basic"
python3 check.py --all
python3 check.py            # 인자 없이 실행해도 전체 채점

# Week2 심화 문제 전체 (01~05) 채점
cd "../2. advanced"
python3 check.py --all

# Week3 기본 문제 전체 (01~09) 채점
cd "../../week3[Python]/1. basic"
python3 check.py --all

# Week3 심화 문제 전체 (01~03) 채점
cd "../2. advanced"
python3 check.py --all
```

특정 문제만 테스트하려면 파일명을 인자로 넘기면 됩니다.

```bash
cd "week2[Python]/1. basic"
python3 check.py 01_string.py
python3 check.py 11_divide_conquer.py
```

### Week2+3 복습 (`week2_3_review`)

```bash
cd week2_3_review
python check.py            # 전체 채점
python check.py 01         # 1번만 채점
python check.py --list     # 문제 목록
python check.py --diff 01  # 틀린 줄 전부 보기
```

막히면 `정답/` 폴더의 참고 코드를 확인하세요. 자세한 설명은 `week2_3_review/README.md` 참고.

### C — `week4[C]`

각 주제 폴더(`Linked_List`, `Stack_and_Queue`, `Binary_Tree`, `Binary_Search_Tree`) 안의
문제지 PDF를 먼저 읽고, `Qn_*.c` 파일의 `TODO` 부분을 채운 뒤 컴파일해서 직접 실행 결과를 확인합니다.

```bash
cd "week4[C]/Binary_Search_Tree"
gcc Q3_F_BST.c -o q3 && ./q3
```

---

## 📜 Advanced 문제 출처

### week2[Python]/2. advanced (5문제)

| 번호 | 문제 | 분류 | 원전 / 출처 | 라이선스 |
|---|---|---|---|---|
| 01 | 퀵 정렬 | 분할정복 응용 | 1961년 C. A. R. Hoare 가 발표한 표준 알고리즘 | 알고리즘 자체는 공지된 표준 기법 |
| 02 | 머지 정렬 | 분할정복 응용 | 1945년 John von Neumann 이 제안한 표준 알고리즘 | 알고리즘 자체는 공지된 표준 기법 |
| 03 | 우선순위 큐 | 힙 자료구조 응용 | 1964년 J. W. J. Williams 의 Heap (heapsort) | 알고리즘 자체는 공지된 표준 기법 |
| 04 | 하노이의 탑 | 재귀 응용 | 1883년 Édouard Lucas (고전 퍼즐) | Public Domain |
| 05 | N-Queen | 백트래킹 응용 | 1848년 Max Bezzel (고전 퍼즐) | Public Domain |

### week3[Python]/2. advanced (3문제)

| 번호 | 문제 | 분류 | 원전 / 출처 | 라이선스 |
|---|---|---|---|---|
| 01 | 위상 정렬 | 그래프 + 큐 + 진입차수 | 1962년 Arthur Kahn 알고리즘 (표준 기법) | 알고리즘 자체는 공지된 표준 기법 |
| 02 | LCS | 2차원 DP (문자열) | 컴퓨터 과학의 표준 DP 문제 | 알고리즘 자체는 공지된 표준 기법 |
| 03 | Dijkstra | 그래프 + heap 최단경로 | 1959년 Edsger W. Dijkstra | 알고리즘 자체는 공지된 표준 기법 |

각 `.py` 파일의 지문과 테스트 케이스는 백준/LeetCode 등 외부 사이트의
지문을 복사하지 않고 본 학습 자료를 위해 자체적으로 작성된 것입니다.

### week4[C]

각 주제 폴더에 동봉된 PDF 문제지(예: `Binary Search Trees Questions.pdf`)를 기준으로
연결 리스트 · 스택/큐 · 이진 트리 · 이진 탐색 트리를 C 언어로 직접 구현하며 학습한 문제들입니다.
