#!/usr/bin/env python3
import subprocess
import itertools
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

# Try to find inputs for all indices 0-1008
print("Searching for inputs that map to each index...")
charset = string.ascii_letters + string.digits + '_'

index_to_input = {}
tested = 0

# Generate inputs systematically
for length in range(1, 25):
    for combo in itertools.product(charset, repeat=min(length, 4)):
        content = ''.join(combo).ljust(24, '0')
        test = f"texsaw{{{content}}}"
        idx = compute_index(test)
        
        if idx not in index_to_input:
            index_to_input[idx] = test
        
        tested += 1
        if tested % 10000 == 0:
            print(f"Tested: {tested}, Found indices: {len(index_to_input)}/1009")
        
        if len(index_to_input) >= 1009:
            break
    if len(index_to_input) >= 1009:
        break

print(f"\nFound inputs for {len(index_to_input)} out of 1009 indices")

# Now test all the indices we found
print("\nTesting all indices for real flags...")
interesting_outputs = []

for idx in sorted(index_to_input.keys()):
    test_input = index_to_input[idx]
    try:
        result = subprocess.run(
            [binary_path, test_input], 
            capture_output=True, 
            text=True, 
            timeout=1
        )
        output = result.stdout.strip()
        
        # Look for success messages or anything that doesn't look like a bash error
        if output and 'SUCCESS' in output:
            interesting_outputs.append((idx, test_input, output))
            print(f"Index {idx:4d}: {output}")
    except:
        pass

print(f"\n{'='*60}")
print(f"Found {len(interesting_outputs)} interesting outputs")
for idx, inp, out in interesting_outputs:
    print(f"Index {idx:4d}: {out}")
