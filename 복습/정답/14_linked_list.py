"""
[복습 14 - 연결 리스트]  (Week2 / 14_linked_list)

핵심 개념:
- 배열과 반대다. 삽입/삭제는 O(1)(노드를 알고 있다면), 인덱스 접근은 O(n).
- 노드를 다룰 땐 '링크를 끊기 전에 다음 노드를 변수에 잡아둔다'가 철칙.
  안 그러면 뒤쪽 전체를 잃어버린다.
- 투 포인터(slow/fast): fast 가 두 칸씩 가면 fast 가 끝에 닿을 때
  slow 는 정확히 가운데에 있다. 사이클 감지에도 같은 원리를 쓴다.

문제:
1) reverse_list(head)
   - 연결 리스트를 뒤집고 새 head 를 반환 (반복문으로, 추가 리스트 없이)
   - 1->2->3 을 3->2->1 로

2) find_middle(head)
   - 가운데 노드의 값을 반환. 노드 개수가 짝수면 '두 번째' 가운데
   - 1->2->3->4 이면 3, 비어있으면 None

3) has_cycle(head)
   - 사이클이 있으면 True (플로이드의 토끼와 거북이)
   - 방문한 노드를 set 에 넣는 방법은 메모리 O(n).
     투 포인터로 하면 메모리 O(1)

힌트:
- 1) prev, cur 두 변수. nxt = cur.next 를 먼저 저장!
- 2) slow 는 한 칸, fast 는 두 칸. while fast and fast.next
- 3) 사이클이 있으면 fast 가 언젠가 slow 를 따라잡는다
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def build(values):
    head = None
    for v in reversed(values):
        node = Node(v)
        node.next = head
        head = node
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.value)
        head = head.next
    return out


def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def find_middle(head):
    if head is None:
        return None
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.value


def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


if __name__ == "__main__":
    print("=== 연결 리스트 뒤집기 ===")
    for values in [[1, 2, 3, 4, 5], [1, 2], [1], []]:
        print(f"{values} -> {to_list(reverse_list(build(values)))}")
    print()

    print("=== 가운데 노드 찾기 ===")
    for values in [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2], [1], []]:
        print(f"{values} -> {find_middle(build(values))}")
    print()

    print("=== 사이클 감지 ===")
    head = build([1, 2, 3, 4])
    print(f"[1,2,3,4] -> {has_cycle(head)}")

    tail = head
    while tail.next:
        tail = tail.next
    tail.next = head.next          # 마지막 노드를 2번 노드에 연결 -> 사이클
    print(f"[1,2,3,4] + 사이클 -> {has_cycle(head)}")

    print(f"[] -> {has_cycle(build([]))}")

    single = build([1])
    single.next = single           # 자기 자신을 가리킴
    print(f"자기 자신을 가리키는 노드 -> {has_cycle(single)}")
