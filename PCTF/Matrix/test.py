#!/usr/bin/env python3
"""
Fixed decryption - extract keystream bytes correctly
"""

# Read keystream states
with open('keystream_leak.txt', 'r') as f:
    states = [int(line.strip()) for line in f.readlines()]

# Read ciphertext
with open('cipher.txt', 'rb') as f:
    ciphertext = f.read()

print(f"[*] Ciphertext length: {len(ciphertext)} bytes")
print(f"[*] Available states: {len(states)}")

# The keystream states are 32-bit values
# Extract bytes from the states properly

keystream_bytes = []

# Method 1: Flatten all bits from states as a byte stream
for state in states:
    # Extract 4 bytes from each 32-bit state (little-endian or big-endian)
    keystream_bytes.append((state >> 0) & 0xFF)
    keystream_bytes.append((state >> 8) & 0xFF)
    keystream_bytes.append((state >> 16) & 0xFF)
    keystream_bytes.append((state >> 24) & 0xFF)

# Trim to match ciphertext length
keystream_bytes = keystream_bytes[:len(ciphertext)]

print(f"[*] Generated {len(keystream_bytes)} keystream bytes")

# Decrypt
plaintext = bytearray()
for i, cipher_byte in enumerate(ciphertext):
    plain_byte = cipher_byte ^ keystream_bytes[i]
    plaintext.append(plain_byte)

print(f"[+] Plaintext (hex): {plaintext.hex()}")
print(f"[+] Plaintext (ascii): {plaintext}")

# Try different interpretations
print("\n[*] Trying different byte orderings...")

# Try big-endian
keystream_bytes_be = []
for state in states:
    keystream_bytes_be.append((state >> 24) & 0xFF)
    keystream_bytes_be.append((state >> 16) & 0xFF)
    keystream_bytes_be.append((state >> 8) & 0xFF)
    keystream_bytes_be.append((state >> 0) & 0xFF)

keystream_bytes_be = keystream_bytes_be[:len(ciphertext)]
plaintext_be = bytearray()
for i, cipher_byte in enumerate(ciphertext):
    plain_byte = cipher_byte ^ keystream_bytes_be[i]
    plaintext_be.append(plain_byte)

print(f"[+] Big-endian plaintext: {plaintext_be}")

# Try state by state (take only first byte of each state)
keystream_bytes_single = []
for state in states:
    keystream_bytes_single.append((state >> 0) & 0xFF)

keystream_bytes_single = keystream_bytes_single[:len(ciphertext)]
plaintext_single = bytearray()
for i, cipher_byte in enumerate(ciphertext):
    plain_byte = cipher_byte ^ keystream_bytes_single[i]
    plaintext_single.append(plain_byte)

print(f"[+] Single byte per state: {plaintext_single}")

# Check for pctf{ pattern
for name, pt in [("LE 4-bytes", plaintext), ("BE 4-bytes", plaintext_be), ("Single byte", plaintext_single)]:
    if b'pctf{' in bytes(pt):
        print(f"\n[!!!] Found flag pattern in {name}:")
        print(f"[+] Flag: {pt}")
        break
    
    # Try decoding as string
    try:
        decoded = pt.decode('utf-8', errors='ignore')
        if 'pctf{' in decoded:
            print(f"\n[!!!] Found flag pattern in {name}:")
            print(f"[+] Flag: {decoded}")
            break
    except:
        pass