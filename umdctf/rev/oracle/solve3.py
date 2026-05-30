import struct, re

with open('oracle','rb') as f:
    data = f.read()

with open('feed.bin','rb') as f:
    feed = f.read()

# ============================================================
# Parameters computed from binary analysis:
# ============================================================
chk_hash = 0x72196a90  # from solve2.py
key_normal = [0x1a2b3c4d, 0x5e6f7081, 0x92a3b4c5, 0xd6e7f809]
key_piped  = [0xc48682a2, 0x5e6f7081, 0x92a3b4c5, 0xd6e7f809]

# xmm0 nonce: 5a5a5a5a5a5a5a5a XOR [0x7020:0x7028]
xmm1_val = struct.unpack_from('Q', data, 0x7020)[0]
xmm0_val = 0x5a5a5a5a5a5a5a5a ^ xmm1_val
nonce_bytes = struct.pack('Q', xmm0_val)
print('[*] Nonce bytes:', nonce_bytes.hex(), repr(nonce_bytes))

# ============================================================
# XTEA encrypt one 8-byte block
# ============================================================
def xtea_enc(v0, v1, key):
    DELTA = 0x9e3779b9
    s = 0
    for _ in range(32):
        v0 = (v0 + (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & 0xffffffff
        v1 = (v1 + (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & 0xffffffff
        s = (s + DELTA) & 0xffffffff
    return v0, v1

def xtea_dec(v0, v1, key):
    DELTA = 0x9e3779b9
    s = (DELTA * 32) & 0xffffffff
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & 0xffffffff
        s = (s - DELTA) & 0xffffffff
    return v0, v1

# ============================================================
# Mode 1: OFB (encrypt nonce, XOR with CT, next nonce = encrypted nonce)
# ============================================================
def xtea_ofb(data_bytes, key, nonce):
    nv0, nv1 = struct.unpack('II', nonce)
    result = bytearray()
    for i in range(0, len(data_bytes), 8):
        ev0, ev1 = xtea_enc(nv0, nv1, key)
        ks = struct.pack('II', ev0, ev1)
        block = data_bytes[i:i+8]
        for j in range(len(block)):
            result.append(block[j] ^ ks[j])
        nv0, nv1 = ev0, ev1
    return bytes(result)

# ============================================================
# Mode 2: CBC decrypt with nonce
# (encrypt nonce, XOR with CT -> plaintext; next nonce = CT block)
# ============================================================
def xtea_cbc(data_bytes, key, nonce):
    nv0, nv1 = struct.unpack('II', nonce)
    result = bytearray()
    for i in range(0, len(data_bytes), 8):
        block = data_bytes[i:i+8]
        if len(block) < 8:
            break
        ev0, ev1 = xtea_enc(nv0, nv1, key)
        ks = struct.pack('II', ev0, ev1)
        for j in range(8):
            result.append(block[j] ^ ks[j])
        nv0, nv1 = struct.unpack('II', block)  # next nonce = original CT
    return bytes(result)

# ============================================================
# Mode 3: Standard XTEA decrypt (ECB)
# ============================================================
def xtea_ecb_dec(data_bytes, key):
    result = bytearray()
    for i in range(0, len(data_bytes), 8):
        v0, v1 = struct.unpack_from('II', data_bytes, i)
        rv0, rv1 = xtea_dec(v0, v1, key)
        result += struct.pack('II', rv0, rv1)
    return bytes(result)

print('\n=== Trying all modes with both keys ===')
for k, kname in [(key_normal, 'tty'), (key_piped, 'piped')]:
    for mode_fn, mname in [(xtea_ofb, 'OFB'), (xtea_cbc, 'CBC'), (xtea_ecb_dec, 'ECB')]:
        if mname == 'ECB':
            decrypted = xtea_ecb_dec(feed, k)
        else:
            decrypted = mode_fn(feed, k, nonce_bytes)
        strings = re.findall(b'[ -~]{6,}', decrypted)
        good_strings = [s for s in strings if s.isalpha() or s.isalnum() or any(c.isalpha() for c in s.decode('ascii', errors='replace'))]
        print(f'{kname}/{mname}: hex={decrypted[:16].hex()} strings={good_strings[:3]}')

# ============================================================
# Maybe the nonce is the full xmm0 (16 bytes)?
# ============================================================
print('\n=== Checking xmm0 construction more carefully ===')
# At 0x127d: lea r9, [rip+0x4d7c]
# rip = 0x127d + 7 = 0x1284? No: lea r9, [rip+imm32] is 7 bytes
# So rip = 0x127d + 7 = 0x1284, target = 0x1284 + 0x4d7c = 0x6000 (!) = .fini!
r9_va = 0x1284 + 0x4d7c
print(f'r9 = rip+0x4d7c from 0x127d: target VA = 0x{r9_va:x}')
print(f'r15 = [0x{r9_va:x}]:', data[r9_va:r9_va+16].hex() if r9_va < len(data) else 'out of range')

# At 0x128b: sub r9, r15  where r15 = [rip+0x3d8b] from 0x126e
r15_target = 0x1275 + 0x3d8b  # 0x126e + 7 = 0x1275, then rip+...
print(f'r15 lea from 0x126e: target = 0x{r15_target:x}')

# Wait, let me use the corrected disasm:
# 0x126e: lea r15, [rip + 0x3d8b]  -> at 0x126e, this is 7 bytes, rip=0x1275
# target = 0x1275 + 0x3d8b = 0x5000 (start of .xtext!)
r15_va = 0x1275 + 0x3d8b
print(f'r15 = 0x{r15_va:x} = start of .xtext section')

# r9 points to something, r12 = r9 - r15 = offset/length of .xtext
# r15 = 0x5000 (.xtext start)
# r9 = 0x6000 (.fini start) -> r12 = r9 - r15 = 0x1000 = size of .xtext
# This is the encrypted .xtext that gets decrypted!

print(f'\n[*] .xtext: VA 0x5000 to 0x6000 (0x1000 bytes), r15=0x5000, r12=0x1000')
print(f'[*] The oracle decrypts .xtext section using XTEA in CBC/OFB mode')
print(f'[*] Then maps it and executes 0x5220 (which is at offset 0x220 in .xtext)')
print(f'[*] Nonce (xmm0): {nonce_bytes.hex()} = {repr(nonce_bytes)}')

xtext = data[0x5000:0x6000]
print(f'\n[*] Trying to decrypt .xtext to verify we have the right key/mode...')
for k, kname in [(key_normal, 'tty'), (key_piped, 'piped')]:
    for mode_fn, mname in [(xtea_ofb, 'OFB'), (xtea_cbc, 'CBC')]:
        decrypted = mode_fn(xtext, k, nonce_bytes)
        # Check for x86 function prologue (push/endbr64 etc)
        has_endbr = decrypted[0:4] == bytes([0xf3, 0x0f, 0x1e, 0xfa])
        has_push = decrypted[0] in [0x55, 0x41, 0x53, 0x48]
        good = 'GOOD!' if (has_endbr or has_push) else ''
        print(f'  {kname}/{mname}: {decrypted[:8].hex()} endbr64={has_endbr} push={has_push} {good}')
