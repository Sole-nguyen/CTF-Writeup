#!/usr/bin/env python3

# The enc() function XORs each byte with 0x1
def enc(s):
    return ''.join(chr(ord(c) ^ 1) for c in s)

# The encrypted string in the binary
encrypted_in_binary = "B1ofs@urX1t4tswhwDeM2w2m1od"

# Decrypt it to get the password we need to enter
password = enc(encrypted_in_binary)

print("=" * 60)
print("JDHACK RPG - Level 1 Solution")
print("=" * 60)
print()
print("Analysis:")
print("-" * 60)
print("1. User input goes through enc() function")
print("2. enc() XORs each character with 0x1")
print("3. Result is compared with:", encrypted_in_binary)
print()
print("Therefore, we need to enter a password that when XOR'd")
print("with 0x1, equals the encrypted string.")
print()
print("Password to enter:", password)
print()
print("The flag format is: JDHACK{password}")
print()
print("=" * 60)
print("FINAL FLAG:", f"JDHACK{{{password}}}")
print("=" * 60)
