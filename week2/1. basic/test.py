def solution(phone_book):
    for i in range(len(phone_book)-1):
        for j in range(i+1,len(phone_book)):
            if phone_book[i] in phone_book[j]:
                return False
    return True

a = ["97674223", "219", "1195524421"]
a =set(a)
if "219" in a:
    print(True)
print(solution(["119", "97674223", "1195524421"]))