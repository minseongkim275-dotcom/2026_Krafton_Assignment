"""
[복습 16 - 이진 트리와 이진 탐색 트리]  (Week3 / 01_binary_tree, 02_bst)

핵심 개념:
- 순회 3형제는 '루트를 언제 방문하는가'만 다르다.
    전위(preorder)  : 루트 -> 왼쪽 -> 오른쪽   (트리 복사, 구조 출력)
    중위(inorder)   : 왼쪽 -> 루트 -> 오른쪽   (BST면 오름차순 정렬!)
    후위(postorder) : 왼쪽 -> 오른쪽 -> 루트   (트리 삭제, 부모가 자식 결과를 쓸 때)
  레벨 순회(level order)만 재귀가 아니라 '큐'를 쓴다.
- BST 규칙: 왼쪽 서브트리 < 노드 < 오른쪽 서브트리.
  탐색/삽입이 평균 O(log h), 하지만 한쪽으로 치우치면 O(n).
- 흔한 함정: "부모보다 크기만 하면 BST"가 아니다.
  오른쪽 자식의 왼쪽 자식도 '조상보다 커야' 한다.
  -> 각 노드에 (하한, 상한) 범위를 물려주며 검사해야 한다.

문제:
1) insert(root, key)
   - BST 에 key 를 넣고 (새) 루트를 반환. 중복 key 는 무시
   - 빈 트리(root=None)면 새 노드가 루트

2) preorder(root) / inorder(root) / postorder(root)
   - 각 순회 결과를 key 리스트로 반환

3) level_order(root)
   - 위에서 아래로, 왼쪽에서 오른쪽으로 방문한 key 리스트 (큐 사용)

4) height(root)
   - 트리의 높이. 빈 트리는 -1, 루트만 있으면 0

5) is_valid_bst(root)
   - 이 트리가 BST 규칙을 지키는지 True/False
   - 중위 순회가 오름차순인지 보는 방법도 있고, 범위를 물려주는 방법도 있다

힌트:
- 1) key < root.key 면 root.left = insert(root.left, key)
- 3) deque 에 루트를 넣고, 꺼낼 때마다 왼쪽/오른쪽 자식을 넣는다
- 4) 1 + max(왼쪽 높이, 오른쪽 높이), 빈 노드는 -1
- 5) check(node, low, high) 로 내려가며 범위를 좁힌다
"""

from collections import deque


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def build(values):
    """리스트를 순서대로 insert 해서 BST 를 만든다 (이미 구현되어 있음)"""
    root = None
    for v in values:
        root = insert(root, v)
    return root


def insert(root, key):
    # TODO: 빈 자리를 찾아 새 노드를 만들고, 루트를 반환
    pass


def preorder(root):
    # TODO: 루트 -> 왼쪽 -> 오른쪽
    pass


def inorder(root):
    # TODO: 왼쪽 -> 루트 -> 오른쪽
    pass


def postorder(root):
    # TODO: 왼쪽 -> 오른쪽 -> 루트
    pass


def level_order(root):
    # TODO: 큐(deque)를 이용한 너비 우선 순회
    pass


def height(root):
    # TODO: 빈 트리는 -1
    pass


def is_valid_bst(root):
    # TODO: (하한, 상한) 범위를 물려주며 검사
    pass


# 테스트 케이스
if __name__ == "__main__":
    #         50
    #      30     70
    #    20  40 60  80
    values = [50, 30, 70, 20, 40, 60, 80]
    root = build(values)

    print("=== 순회 ===")
    print(f"삽입 순서 : {values}")
    print(f"전위(pre) : {preorder(root)}")
    print(f"중위(in)  : {inorder(root)}")
    print(f"후위(post): {postorder(root)}")
    print(f"레벨(bfs) : {level_order(root)}")
    print()

    print("=== 중위 순회는 정렬된 결과여야 한다 ===")
    print(f"{inorder(root)} == {sorted(values)} -> {inorder(root) == sorted(values)}")
    print()

    print("=== 높이 ===")
    for vals in [[50, 30, 70, 20, 40, 60, 80], [1, 2, 3, 4, 5], [10], []]:
        tree = build(vals)
        print(f"{vals} -> 높이 {height(tree)}")
    print()

    print("=== 중복 삽입은 무시 ===")
    dup = build([5, 3, 5, 3, 7])
    print(f"[5,3,5,3,7] -> {inorder(dup)}")
    print()

    print("=== BST 유효성 검사 ===")
    print(f"정상 BST -> {is_valid_bst(root)}")

    # 얼핏 보면 부모-자식 관계는 맞지만 BST 가 아닌 트리
    bad = TreeNode(10)
    bad.left = TreeNode(5)
    bad.right = TreeNode(15)
    bad.right.left = TreeNode(6)      # 10의 오른쪽인데 10보다 작다
    print(f"잘못된 트리 -> {is_valid_bst(bad)}")
    print(f"  (중위 순회: {inorder(bad)})")
    print(f"빈 트리 -> {is_valid_bst(None)}")
    print(f"노드 하나 -> {is_valid_bst(TreeNode(1))}")
