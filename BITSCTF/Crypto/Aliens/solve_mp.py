#!/usr/bin/env python3

from aes import AES
from multiprocessing import Pool, cpu_count

with open('output.txt', 'r') as f:
    lines = f.readlines()

key_hint = lines[0].split(': ')[1].strip()
encrypted_flag = bytes.fromhex(lines[1].split(': ')[1].strip())
num_samples = int(lines[2].split(': ')[1].strip())

samples = []
for i in range(4, 4 + num_samples):
    plaintext_hex, ciphertext_hex = lines[i].strip().split(',')
    samples.append((bytes.fromhex(plaintext_hex), bytes.fromhex(ciphertext_hex)))

key_hint_bytes = bytes.fromhex(key_hint)

def check_key(b1):
    for b2 in range(256):
        for b3 in range(256):
            candidate_key = key_hint_bytes + bytes([b1, b2, b3])
            cipher = AES(candidate_key)
            test_ct = cipher.encrypt(samples[0][0])
            if test_ct == samples[0][1]:
                valid = True
                for i in range(min(10, len(samples))):
                    if cipher.encrypt(samples[i][0]) != samples[i][1]:
                        valid = False
                        break
                if valid:
                    return candidate_key
    return None

if __name__ == '__main__':
    with Pool(cpu_count()) as pool:
        results = pool.map(check_key, range(256))
    
    for result in results:
        if result:
            print(f"Found key: {result.hex()}")
            cipher = AES(result)
            flag = b""
            for i in range(0, len(encrypted_flag), 16):
                block = encrypted_flag[i:i+16]
                decrypted_block = cipher.decrypt(block)
                flag += decrypted_block
            flag = flag.rstrip(b'\x00')
            print(f"FLAG: {flag.decode('ascii', errors='ignore')}")
            break
