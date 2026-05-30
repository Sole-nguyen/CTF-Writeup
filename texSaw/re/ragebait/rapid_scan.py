#!/usr/bin/env python3
import subprocess
import random
import string

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

print("Rapidly testing many random inputs...")
charset = string.ascii_letters + string.digits + '_'

tested_indices = set()
unique_outputs = {}

attempts = 0
while len(tested_indices) < 1009 and attempts < 1000000:
    content = ''.join(random.choice(charset) for _ in range(24))
    test = f"texsaw{{{content}}}"
    idx = compute_index(test)
    
    if idx in tested_indices:
        attempts += 1
        continue
    
    tested_indices.add(idx)
    
    try:
        result = subprocess.run([binary_path, test], capture_output=True, text=True, timeout=0.5)
        output = result.stdout.strip()
        
        if output:
            if output not in unique_outputs:
                unique_outputs[output] = []
            unique_outputs[output].append((idx, test))
    except:
        pass
    
    attempts += 1
    if attempts % 1000 == 0:
        print(f"Attempts: {attempts}, Indices tested: {len(tested_indices)}, Unique outputs: {len(unique_outputs)}")

print(f"\n{'='*60}")
print(f"Final: {len(tested_indices)} indices tested, {len(unique_outputs)} unique outputs found")
print(f"{'='*60}\n")

# Print all unique outputs sorted
for output in sorted(unique_outputs.keys()):
    indices = unique_outputs[output]
    if 'SUCCESS' in output or 'texsaw{' in output.lower():
        print(f"\n{output}")
        print(f"  Found at {len(indices)} indices, first few: {[i[0] for i in indices[:3]]}")
