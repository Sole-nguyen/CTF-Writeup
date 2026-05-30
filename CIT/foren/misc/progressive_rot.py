def rot(char, n):
    if 'A' <= char <= 'Z':
        return chr((ord(char) - ord('A') + n) % 26 + ord('A'))
    return char

text = "KLEGCKRGGONTBNBVPIIZWXQQEZYAXXWQMGIZDNEWWUTOVZRWOMZKGWNKWZBQXOGZSTVCGU"

print("Progressive ROT (n+1):")
res = ""
for i, char in enumerate(text):
    res += rot(char, -(i+1))
print(res)

print("\nProgressive ROT (n):")
res = ""
for i, char in enumerate(text):
    res += rot(char, -i)
print(res)
