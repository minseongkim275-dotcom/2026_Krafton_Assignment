"""
[복습 09 - 정수론]  (Week2 / 09_number_theory)

핵심 개념:
- 소수 판별에서 2부터 n-1 까지 다 보면 O(n).
  약수는 항상 쌍(d, n/d)으로 생기고 둘 중 작은 쪽은 sqrt(n) 이하이므로
  i*i <= n 까지만 보면 된다 -> O(sqrt n).
- 여러 개를 한꺼번에 판별할 땐 에라토스테네스의 체 O(n log log n).
  i의 배수를 지울 때 i*i 부터 시작하면 된다 (그 앞은 이미 지워졌다).
- 유클리드 호제법: gcd(a, b) = gcd(b, a % b), b가 0이면 a가 답.
- lcm(a, b) = a * b / gcd(a, b)  ->  오버플로 피하려면 a // gcd * b

문제:
1) is_prime(n)
   - n 이 소수면 True. 1 이하는 False. O(sqrt n) 으로!

2) sieve(n)
   - n 이하의 모든 소수를 리스트로 반환 (에라토스테네스의 체)
   - n < 2 면 빈 리스트

3) gcd(a, b) / lcm(a, b)
   - 최대공약수(유클리드 호제법, 반복문), 최소공배수
   - 둘 중 하나가 0이면 lcm 은 0

4) prime_factors(n)
   - n 의 소인수분해 결과를 오름차순 리스트로 (중복 포함)
   - 12 -> [2,2,3], 97 -> [97], 1 -> []

힌트:
- 1) while i * i <= n
- 2) [True] * (n+1) 배열을 만들고 0, 1 을 False 로
- 3) while b: a, b = b, a % b
- 4) 2부터 나눌 수 있을 때까지 계속 나누고, 남은 값이 1보다 크면 그것도 소인수
"""

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def sieve(n):
    if n < 2:
        return []
    flag = [True] * (n + 1)
    flag[0] = flag[1] = False
    i = 2
    while i * i <= n:
        if flag[i]:
            for j in range(i * i, n + 1, i):
                flag[j] = False
        i += 1
    return [i for i, prime in enumerate(flag) if prime]


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return a // gcd(a, b) * b


def prime_factors(n):
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


if __name__ == "__main__":
    print("=== 소수 판별 ===")
    for n in [0, 1, 2, 3, 4, 17, 25, 97, 100, 7919]:
        print(f"{n} -> {is_prime(n)}")
    print()

    print("=== 에라토스테네스의 체 ===")
    for n in [1, 10, 30, 50]:
        print(f"{n} 이하 소수: {sieve(n)}")
    print(f"100 이하 소수 개수: {len(sieve(100))}")
    print(f"1000 이하 소수 개수: {len(sieve(1000))}")
    print()

    print("=== 체와 판별 결과가 일치하는지 ===")
    by_sieve = sieve(200)
    by_check = [n for n in range(201) if is_prime(n)]
    print(f"일치: {by_sieve == by_check}")
    print()

    print("=== 최대공약수 / 최소공배수 ===")
    for a, b in [(12, 18), (100, 75), (17, 5), (0, 7), (24, 24)]:
        print(f"gcd({a}, {b}) = {gcd(a, b)}, lcm({a}, {b}) = {lcm(a, b)}")
    print()

    print("=== 소인수분해 ===")
    for n in [1, 12, 60, 97, 1024, 999]:
        print(f"{n} -> {prime_factors(n)}")
