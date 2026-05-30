# -*- coding: utf-8 -*-
"""
Since we can't find the pattern, let's just BRUTE FORCE the remaining keys!
We know the first 8 and last 1, so we need to find 33 bytes.

For each unknown position, try all 256 values and see which gives printable ASCII
"""

data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

# Known XOR keys
known_keys = {
    0: 16, 1: 217, 2: 239, 3: 20, 4: 161, 5: 71, 6: 98, 7: 128,
    41: 61  # Last byte should be '}' (0x7d)
}

print("Brute forcing unknown XOR keys...")
print("Looking for combinations that produce readable text\n")

# Initialize keys array
keys = [0] * 42
for pos, key in known_keys.items():
    keys[pos] = key

# For unknown positions, try all values that give printable ASCII
candidates_per_position = {}

for pos in range(42):
    if pos in known_keys:
        continue
    
    candidates = []
    for key_val in range(256):
        plain = data[pos] ^ key_val
        if 32 <= plain < 127:  # Printable ASCII
            candidates.append((key_val, chr(plain)))
    
    candidates_per_position[pos] = candidates
    print(f"Position {pos:2d}: {len(candidates):3d} candidates")

print(f"\nTotal unknown positions: {len(candidates_per_position)}")

# Now try to use context to narrow down
# Start with a greedy approach: pick the most common character at each position

print("\n" + "="*60)
print("Attempting greedy decode (picking most common letters)...")
print("="*60)

for pos in range(42):
    if pos in known_keys:
        continue
    
    if pos in candidates_per_position:
        # Prefer alphanumeric characters
        candidates = candidates_per_position[pos]
        
        # Scoring: prefer a-z, A-Z, 0-9, then common punctuation
        def score_char(c):
            if c.isalnum():
                return 100
            if c in '_-':
                return 50
            return 10
        
        best = max(candidates, key=lambda x: score_char(x[1]))
        keys[pos] = best[0]

# Decode with guessed keys
result = bytes([data[i] ^ keys[i] for i in range(42)])

try:
    text = result.decode('ascii')
    print(f"\nGuessed flag: {text}")
    
    if text.startswith('uoftctf{') and text.endswith('}'):
        print("\n✓ Flag format looks correct!")
    else:
        print("\n⚠ Flag format doesn't match expected pattern")
except Exception as e:
    print(f"\nDecode failed: {e}")

print(f"\nGuessed XOR keys: {[f'0x{k:02x}' for k in keys]}")
