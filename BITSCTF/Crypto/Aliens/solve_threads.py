#!/usr/bin/env python3

from aes import AES
import concurrent.futures

# Read the output file
with open('output.txt', 'r') as f:
    lines = f.readlines()

# Parse the data
key_hint = lines[0].split(': ')[1].strip()
encrypted_flag = bytes.fromhex(lines[1].split(': ')[1].strip())

# Parse samples  
samples = []
for i in range(4, 1004):
    plaintext_hex, ciphertext_hex = lines[i].strip().split(',')
    samples.append((bytes.fromhex(plaintext_hex), bytes.fromhex(ciphertext_hex)))

key_hint_bytes = bytes.fromhex(key_hint)
print(f"Known key bytes: {key_hint_bytes.hex()} ({len(key_hint_bytes)} bytes)")
print(f"Need to find: 3 bytes")
print(f"Total combinations: {256**3} = 16,777,216")

def test_key(args):
    """Test a specific key candidate"""
    b1, b2, b3 = args
    candidate_key = key_hint_bytes + bytes([b1, b2, b3])
    
    try:
        cipher = AES(candidate_key)
        # Quick test with first sample
        if cipher.encrypt(samples[0][0]) == samples[0][1]:
            # Verify with 5 more samples
            if all(cipher.encrypt(samples[i][0]) == samples[i][1] for i in range(1, 6)):
                return (True, candidate_key, b1, b2, b3)
    except:
        pass
    
    return (False, None, b1, b2, b3)

# Generate all combinations
all_keys = [(b1, b2, b3) for b1 in range(256) for b2 in range(256) for b3 in range(256)]

print("Starting parallel brute force with thread pool...")
found = False

with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(test_key, k): k for k in all_keys}
    
    completed = 0
    for future in concurrent.futures.as_completed(futures):
        completed += 1
        if completed % 50000 == 0:
            print(f"Progress: {completed}/{len(all_keys)} ({100*completed/len(all_keys):.1f}%)")
        
        success, key, b1, b2, b3 = future.result()
        if success:
            print(f"\n✓ Found key: {key.hex()}")
            print(f"  Last 3 bytes: {b1:02x} {b2:02x} {b3:02x}")
            
            # Cancel remaining futures
            for f in futures:
                f.cancel()
            
            # Decrypt the flag
            print("\nDecrypting flag...")
            cipher = AES(key)
            flag = b""
            for j in range(0, len(encrypted_flag), 16):
                block = encrypted_flag[j:j+16]
                decrypted_block = cipher.decrypt(block)
                flag += decrypted_block
            
            # Remove padding
            flag = flag.rstrip(b'\x00')
            print(f"\n🚩 FLAG: {flag.decode('ascii', errors='ignore')}")
            found = True
            break

if not found:
    print("\nKey not found!")
