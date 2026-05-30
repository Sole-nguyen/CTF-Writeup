#!/usr/bin/env python3
"""
Fast PoW solver using optimized algorithm
The PoW is: y -> (y^1)^2 mod M for 5000 iterations
We need to find y such that result == target
"""
import base64
import struct

POW_MOD = (1 << 1279) - 1

def decode_challenge(value):
    parts = value.split('.', 2)
    d_bytes = base64.b64decode(parts[1])
    padded = b'\x00' * (4 - len(d_bytes)) + d_bytes
    difficulty = struct.unpack('>I', padded)[0]
    x_bytes = base64.b64decode(parts[2])
    x = int.from_bytes(x_bytes, 'big') if x_bytes else 0
    return difficulty, x

# Use the challenge from the website
challenge = "s.AAATiA==.bizEEHS67/+hKOLsVwocUQ=="
difficulty, target = decode_challenge(challenge)

print(f"Difficulty: {difficulty}, Target: {target}")
print(f"Trying small values...")

# The key insight: for small y values, this converges quickly
# Try y from 0 to 1000
for y in range(1000):
    current = y
    for i in range(difficulty):
        current = (current ^ 1)
        current = (current * current) % POW_MOD
    
    if current == target or current == (POW_MOD - target):
        y_bytes = y.to_bytes((y.bit_length() + 7) // 8 or 1, 'big')
        solution = f"s.{base64.b64encode(y_bytes).decode()}"
        print(f"\nSolution found! y={y}")
        print(f"Solution: {solution}")
        break
else:
    print("No solution in range 0-1000")
