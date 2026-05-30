#!/usr/bin/env python3
import subprocess
import random
import string

binary_path = './ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY'

# FNV-1a hash function
def fnv1a_hash(data):
    """Compute FNV-1a hash"""
    hash_value = 0x811c9dc5
    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * 0x1000193) & 0xFFFFFFFF
    return hash_value

def compute_index(input_str):
    """Compute the index used to select function from table"""
    data = input_str[9:].encode()
    hash_val = fnv1a_hash(data)
    
    temp = (hash_val * 0x3ce4585) >> 32
    result = hash_val - temp
    result = result >> 1
    result = result + temp
    result = result >> 9
    index = hash_val - (result * 0x3f1)
    
    return index

print("Testing different inputs to find the real flag...")
print("=" * 60)

# The input must be 32 characters long
# texsaw{XXXXXXXXXXXXXXXXXXXXXXXX}
#   7     +     24    +        1   = 32

# Let's try to systematically test different indices
charset = string.ascii_letters + string.digits + '_'

# Keep track of unique outputs
seen_outputs = set()
tested_indices = set()

# Try random combinations
for attempt in range(100000):
    # Generate random 24-character content
    content = ''.join(random.choice(charset) for _ in range(24))
    test_input = f"texsaw{{{content}}}"
    
    idx = compute_index(test_input)
    
    # Skip if we've tested this index
    if idx in tested_indices:
        continue
    tested_indices.add(idx)
    
    try:
        result = subprocess.run(
            [binary_path, test_input], 
            capture_output=True, 
            text=True, 
            timeout=1
        )
        
        output = result.stdout.strip()
        
        # Check if we got new output
        if output and output not in seen_outputs:
            seen_outputs.add(output)
            print(f"Index {idx:4d}: {output}")
            
            # Check if it looks like a real flag (not the fake one)
            if 'texsaw{' in output and 'n0t_th3_fl4g_lol' not in output:
                print(f"\n{'='*60}")
                print(f"POTENTIAL REAL FLAG FOUND!")
                print(f"Input: {test_input}")
                print(f"Output: {output}")
                print(f"{'='*60}\n")
    
    except Exception as e:
        pass
    
    if attempt % 1000 == 0:
        print(f"Progress: {attempt} attempts, {len(tested_indices)} unique indices tested, {len(seen_outputs)} unique outputs")

print(f"\nTotal unique outputs found: {len(seen_outputs)}")
print("\nAll unique outputs:")
for output in sorted(seen_outputs):
    print(f"  {output}")
