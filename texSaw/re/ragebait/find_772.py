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

# Find input for index 772 (the long fake flag)
print("Searching for index 772...")
for length in range(1, 25):
    found = False
    for combo in itertools.product(string.ascii_letters + string.digits + '_', repeat=min(length, 6)):
        content = ''.join(combo).ljust(24, '0')
        test = f"texsaw{{{content}}}"
        idx = compute_index(test)
        
        if idx == 772:
            print(f"Found input for index 772: {test}")
            result = subprocess.run([binary_path, test], capture_output=True, text=True)
            print(f"Output: {result.stdout}")
            found = True
            break
    if found:
        break
