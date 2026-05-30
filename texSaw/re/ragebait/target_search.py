#!/usr/bin/env python3
import subprocess
import string
import itertools

binary_path = './ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY'

def fnv1a_hash(data):
    hash_value = 0x811c9dc5
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * 0x1000193) & 0xFFFFFFFF
    return hash_value

def compute_index(input_str):
    data = input_str[9:].encode()
    hash_val = fnv1a_hash(data)
    temp = (hash_val * 0x3ce4585) >> 32
    result = hash_val - temp
    result = result >> 1
    result = result + temp
    result = result >> 9
    index = hash_val - (result * 0x3f1)
    return index

# Target specific "interesting" indices
target_indices = [0, 1, 42, 69, 420, 666, 1337 % 1009, 1000, 1008, 500]

print("Searching for inputs that map to interesting indices...")
charset = string.printable.strip()

found = {}

# Brute force search for these specific indices
for target in target_indices:
    print(f"\nSearching for index {target}...")
    found_for_target = False
    
    for length in range(1, 25):
        if found_for_target:
            break
        for combo in itertools.product(string.ascii_letters + string.digits + '_', repeat=min(length, 6)):
            content = ''.join(combo).ljust(24, '0')
            test = f"texsaw{{{content}}}"
            idx = compute_index(test)
            
            if idx == target:
                found[target] = test
                print(f"  Found: {test}")
                found_for_target = True
                break

print(f"\n{'='*60}")
print("Testing found inputs...")
print('='*60)

for idx, inp in sorted(found.items()):
    try:
        result = subprocess.run(
            [binary_path, inp], 
            capture_output=True, 
            text=True, 
            timeout=1
        )
        output = result.stdout.strip()
        if not output:
            output = result.stderr.strip()
        print(f"Index {idx:4d}: {output if output else '(no output)'}")
    except Exception as e:
        print(f"Index {idx:4d}: Error - {e}")
