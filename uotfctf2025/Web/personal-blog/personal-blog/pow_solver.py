#!/usr/bin/env python3
import base64
import struct
import sys

POW_VERSION = 's'
POW_MOD = (1 << 1279) - 1
POW_ONE = 1

def decode_challenge(value):
    parts = value.split('.', 2)
    if len(parts) != 3 or parts[0] != POW_VERSION:
        return None
    
    d_bytes = base64.b64decode(parts[1])
    padded = b'\x00' * (4 - len(d_bytes)) + d_bytes
    difficulty = struct.unpack('>I', padded)[0]
    
    x_bytes = base64.b64decode(parts[2])
    x = int.from_bytes(x_bytes, 'big') if x_bytes else 0
    
    return {'difficulty': difficulty, 'x': x}

def solve_pow(challenge):
    decoded = decode_challenge(challenge)
    if not decoded:
        return None
    
    difficulty = decoded['difficulty']
    target = decoded['x']
    
    print(f"[*] Difficulty: {difficulty}")
    print(f"[*] Target: {target}")
    print(f"[*] Solving...")
    
    # Try values from 0 to a reasonable limit
    max_attempts = 10000000
    for y in range(max_attempts):
        if y % 100000 == 0 and y > 0:
            print(f"[*] Tried {y} values...")
        
        current = y
        for i in range(difficulty):
            current = (current ^ POW_ONE)
            current = (current * current) % POW_MOD
        
        if current == target or current == (POW_MOD - target):
            y_bytes = y.to_bytes((y.bit_length() + 7) // 8 or 1, 'big')
            solution = f"{POW_VERSION}.{base64.b64encode(y_bytes).decode()}"
            print(f"[+] Found solution: {solution} (y={y})")
            return solution
    
    return None

if __name__ == '__main__':
    challenge = "s.AAATiA==.bizEEHS67/+hKOLsVwocUQ=="
    print(f"[*] Challenge: {challenge}")
    solution = solve_pow(challenge)
    if solution:
        print(f"\n[+] Solution: {solution}")
    else:
        print("\n[-] No solution found")
