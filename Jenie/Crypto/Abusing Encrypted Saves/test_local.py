#!/usr/bin/env python3
import json
import base64

# Test the bit-flipping approach with known values

def xor_bytes(b1, b2):
    """XOR two byte strings"""
    return bytes(a ^ b for a, b in zip(b1, b2))

# From a real save (you got a win!)
original_stats = {"wins": "001", "losses": "000", "draws": "000", "total_games": "001", "winrate": "100.0"}
original_plaintext = json.dumps(original_stats).encode()

# Target stats
target_stats = {"wins": "100", "losses": "000", "draws": "000", "total_games": "100", "winrate": "100.00"}
target_plaintext = json.dumps(target_stats).encode()

print(f"Original: {original_plaintext}")
print(f"Original len: {len(original_plaintext)}")
print(f"Target:   {target_plaintext}")
print(f"Target len: {len(target_plaintext)}")

# The target is ONE byte longer (100.00 vs 100.0)
# This is a problem! We need exact same length

# Better approach: just modify the wins and total_games fields
# If we already have a win, we just need to change "001" to "100" in two places

print("\n=== Analysis ===")
print(f"Original plaintext: {original_plaintext.decode()}")
print(f"Need to change: '001' -> '100' in wins field")
print(f"Need to change: '001' -> '100' in total_games field")
print(f"Winrate is already 100.0 (or need to fix decimal places)")

# Find positions
pos1 = original_plaintext.find(b'"wins": "001"')
pos2 = original_plaintext.find(b'"total_games": "001"')

print(f"\nPosition of wins '001': {pos1}")
print(f"Position of total_games '001': {pos2}")
