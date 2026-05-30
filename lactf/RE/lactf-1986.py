import string

# Ciphertext bytes
cipher = bytes.fromhex("b68c958f9b854c5eecb6b8c097930b587750b02c7e287af1b604efbe5c4478e89981048f0340a73ffab708016352e3add1859f9421d52a5c20d43112ceaa16c7addf295d72fc24902c00")

def decrypt_chunk(start_idx, length, seed):
    res = ""
    mask = seed
    for i in range(length):
        if start_idx + i >= len(cipher): break
        
        c = cipher[start_idx + i]
        
        # The logic we found works best:
        # 1. Invert mask (~mask)
        # 2. XOR with cipher
        # 3. Strip top bit (& 0x7F)
        val = (c ^ (~mask & 0xFF)) & 0x7F
        
        res += chr(val)
        mask >>= 1
    return res

def score_text(text):
    # Simple scorer: prefers letters, numbers, and underscore
    score = 0
    for c in text:
        if c in string.ascii_letters + string.digits: score += 2
        elif c in "{}_": score += 3
        elif c in string.printable: score += 0
        else: score -= 50
    return score

print(f"{'Block':<5} | {'Seed':<4} | {'Decoded Text':<20} | {'Score'}")
print("-" * 50)

# 1. Block 0 (Indices 0-5) - Known Seed 0x25
b0 = decrypt_chunk(0, 6, 0x25)
print(f"0 (00) | 0x25 | {b0:<20} | [FIXED]")
full_flag = b0

# 2. Subsequent blocks (Indices 6, 14, 22...) - Length 8
# We brute force the seed for each 8-byte chunk
curr_idx = 6

while curr_idx < len(cipher):
    best_text = ""
    best_score = -9999
    best_seed = 0
    
    # Try all seeds
    for s in range(256):
        txt = decrypt_chunk(curr_idx, 8, s)
        sc = score_text(txt)
        
        if sc > best_score:
            best_score = sc
            best_text = txt
            best_seed = s
            
    print(f"{curr_idx // 8:<5} | 0x{best_seed:02x} | {best_text:<20} | {best_score}")
    full_flag += best_text
    curr_idx += 8

print("-" * 50)
print(f"FLAG: {full_flag}")