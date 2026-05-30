#!/usr/bin/env python3
"""
PoW Solver for Personal Blog CTF
Based on the server.js PoW implementation
"""
import base64
import struct

POW_VERSION = 's'
POW_MOD = (1 << 1279) - 1
POW_ONE = 1

def bytes_to_bigint(buf):
    if not buf:
        return 0
    return int.from_bytes(buf, 'big')

def decode_challenge(value):
    parts = value.split('.', 2)
    if len(parts) != 3 or parts[0] != POW_VERSION:
        return None
    
    d_bytes = base64.b64decode(parts[1])
    if len(d_bytes) > 4:
        return None
    
    padded = b'\x00' * (4 - len(d_bytes)) + d_bytes
    difficulty = struct.unpack('>I', padded)[0]
    x_bytes = base64.b64decode(parts[2])
    x = bytes_to_bigint(x_bytes)
    
    return {'difficulty': difficulty, 'x': x}

def solve_pow(challenge):
    """
    Solve the PoW challenge
    We need to find y such that after 'difficulty' iterations:
    y -> (y XOR 1) -> square mod POW_MOD -> ... -> x
    """
    decoded = decode_challenge(challenge)
    if not decoded:
        print("Failed to decode challenge")
        return None
    
    difficulty = decoded['difficulty']
    target = decoded['x']
    
    print(f"[*] Difficulty: {difficulty}")
    print(f"[*] Target: {hex(target)[:50]}...")
    
    # This is a square root chain problem
    # We need to reverse: y -> (y^1)^2 -> ((y^1)^2^1)^2 -> ...
    # Going backwards is hard, so we'll try forward search
    
    # For small difficulties, we can brute force
    if difficulty > 100:
        print(f"[!] Difficulty too high for simple solve: {difficulty}")
        return None
    
    print(f"[*] Attempting to solve (this may take a while)...")
    
    # Try different y values
    for y in range(0, 100000000):
        if y % 1000000 == 0:
            print(f"[*] Tried {y} values...")
        
        current = y
        for i in range(difficulty):
            current = (current ^ POW_ONE)
            current = (current * current) % POW_MOD
        
        if current == target or current == (POW_MOD - target):
            y_bytes = y.to_bytes((y.bit_length() + 7) // 8 or 1, 'big')
            solution = f"{POW_VERSION}.{base64.b64encode(y_bytes).decode()}"
            print(f"[+] Found solution: {solution}")
            return solution
    
    print(f"[-] No solution found in range")
    return None

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: solve_pow.py <challenge>")
        print("Example: solve_pow.py 's.AAATiA==.7+bEH2ggsreV3NaxMgLjpA=='")
        sys.exit(1)
    
    challenge = sys.argv[1]
    solution = solve_pow(challenge)
    if solution:
        print(f"\n[+] Solution: {solution}")
    else:
        print(f"\n[-] Could not solve PoW")
