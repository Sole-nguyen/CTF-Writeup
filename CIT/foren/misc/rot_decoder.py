def rot(text, n):
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + n) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + n) % 26 + ord('a'))
        else:
            result += char
    return result

text = "KLEGCKRGGONTBNBVPIIZWXQQEZYAXXWQMGIZDNEWWUTOVZRWOMZKGWNKWZBQXOGZSTVCGU"
for i in range(1, 26):
    print(f"ROT{i:02d}: {rot(text, i)}")
