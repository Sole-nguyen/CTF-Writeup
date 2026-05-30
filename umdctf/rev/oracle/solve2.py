import struct
import re

with open('oracle','rb') as f:
    data = f.read()

# ============================================================
# Step 1: Compute hash of chk section
# ============================================================
chk_start = 0x4340
chk_end = 0x457e
chk_data = data[chk_start:chk_end]

ebx = 0xc0def1ab
for byte_val in chk_data:
    eax = (byte_val ^ ebx) & 0xffffffff
    eax = (eax * 0x5bd1e995) & 0xffffffff
    ebx_shifted = (eax >> 0xf) & 0xffffffff
    ebx = (ebx_shifted ^ eax) & 0xffffffff
    
chk_hash = ebx
print(f'[*] chk section hash: 0x{chk_hash:08x}')

# ============================================================
# Step 2: Derive XTEA key
# ============================================================
table1 = [struct.unpack_from('<I', data, 0x7000 + i*4)[0] for i in range(4)]
table2 = [struct.unpack_from('<I', data, 0x7010 + i*4)[0] for i in range(4)]

key_normal = [(table1[i] ^ chk_hash ^ table2[i]) & 0xffffffff for i in range(4)]
key_piped  = [key_normal[0] ^ 0xdeadbeef] + key_normal[1:]

print(f'[*] XTEA key (tty):   {[hex(k) for k in key_normal]}')
print(f'[*] XTEA key (piped): {[hex(k) for k in key_piped]}')

# ============================================================
# Step 3: XTEA decryption 
# ============================================================
def xtea_decrypt(ct, key):
    DELTA = 0x9e3779b9
    ROUNDS = 32
    result = b''
    for i in range(0, len(ct), 8):
        v0, v1 = struct.unpack('<II', ct[i:i+8])
        s = (DELTA * ROUNDS) & 0xffffffff
        for _ in range(ROUNDS):
            v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & 0xffffffff
            v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & 0xffffffff
            s = (s - DELTA) & 0xffffffff
        result += struct.pack('<II', v0, v1)
    return result

with open('feed.bin','rb') as f:
    feed = f.read()

print(f'[*] feed.bin: {len(feed)} bytes = {len(feed)//8} XTEA blocks')

for k, kname in [(key_normal, 'tty'), (key_piped, 'piped')]:
    decrypted = xtea_decrypt(feed, k)
    print(f'\n=== Decrypted with {kname} key ===')
    print(f'  hex: {decrypted[:32].hex()}')
    strings = re.findall(b'[ -~]{4,}', decrypted)
    print(f'  strings: {strings[:10]}')
    print(f'  magic[0:4]: {decrypted[:4]}')

# ============================================================
# Step 4: Understand ticket validation
# The ticket structure:
#   TKT\x01 + uint32 payload_size + payload_bytes
# Given sample: 544b54 01 20000000 + 32 bytes
# So payload_size=0x20=32, payload=32 bytes
#
# The main function at 0x2940 is called with:
#   rdi = key (16 bytes at rsp+0x20)
#   rsi = xmm0 value (from [rsp+0x30] = 8 bytes from pshuflw)  
#   rdx = r15 = some address
#   rcx = r12 = some length
# And it decrypts the feed.bin
#
# But we need to understand what 0x5220 does (the .xtext function that processes ticket)
# .xtext is ENCRYPTED and decrypted at runtime by the mmap syscall + function at 0x2940
# So we need to first decrypt the feed.bin to understand the oracle protocol
# ============================================================

# ============================================================
# Step 5: Also check the AES key expansion hint
# At 0x126c:  mov ch, cl   <- ch = cl (byte that was read from stdin)
# movq xmm1, [rip+0x5da3]  from 0x127d: rip=0x1284, target=0x1284+0x5da3=0x7027? no
# 0x127d: movq xmm1, [rip+0x5da3] -- 8 bytes: rip=0x1285, target=0x1285+0x5da3=0x7028
# (or rip = 0x127d+8=0x1285)
# 0x7028 in rodata:
print()
print('[*] xmm1 source (0x7028):')
xmm1_data = data[0x7028:0x7030]
print(f'   {xmm1_data.hex()}')
print(f'   as int64: 0x{struct.unpack("<Q", xmm1_data)[0]:016x}')

# pshuflw xmm0, xmm2, 0 -> broadcast low word of xmm2 into all 4 words of low qword
# xmm2 was from movd xmm2, ecx where ecx contained ch in byte cl:
# ch = cl AND 0xff (low byte of cl put in ch position = byte value * 0x100)
# Actually: mov ch, cl -> ecx[8:16] = ecx[0:8]. So ecx = (cl << 8) | cl = cl * 0x101
# Wait: ecx was from movzx ecx, byte ptr [rsp+0x1f] where [rsp+0x1f] = 0x5a
# So ecx = 0x5a. Then mov ch, cl -> ch = 0x5a, so ecx = 0x5a5a
# movd xmm2, ecx -> xmm2 = 0x00005a5a
# pshuflw xmm0, xmm2, 0 -> broadcast 0x5a5a to all 4 words of low qword
# xmm0 = 0x5a5a5a5a5a5a5a5a (lower 8 bytes)
# pxor xmm0, xmm1 -> xmm0 ^= xmm1

# This is the XOR mask for the AES key!
# Actually it's the stdin input verification key...
# The "stdin input" is what the user types when running the binary interactively
# Looking at 0x4370 (chk section): it reads from fd=2 (stderr? tty?)
# Matches 10 chars against a key (computed from 0x5a XOR stuff), then reads a number

# The 10-char match check in chk (0x4476-0x4498):
# Compares bytes [rax] vs [rcx] for 10 bytes
# [rcx] = [rsp+0x20] = the 8-byte XOR result (xmm0 after pxor) but only 8 chars?
# [rsp+0x28] and [rsp+0x29] are set to extra bytes

# Let me compute what the expected 10-char sequence is:
# ecx starts as 0x5a (the Z byte), ch = cl -> ecx = 0x5a5a
# xmm0 gets pshuflw'd to fill low 64 bits with 0x5a5a repeated 4x = 0x5a5a5a5a5a5a5a5a
# pxor xmm0, xmm1 where xmm1 = 8 bytes from 0x7028

xmm1_val = struct.unpack('<Q', xmm1_data)[0]
xmm0_before = 0x5a5a5a5a5a5a5a5a
xmm0_after = xmm0_before ^ xmm1_val

print(f'\n[*] xmm0 before pxor: 0x{xmm0_before:016x}')
print(f'[*] xmm1: 0x{xmm1_val:016x}')
print(f'[*] xmm0 after pxor: 0x{xmm0_after:016x}')

key_bytes = struct.pack('<Q', xmm0_after)
print(f'[*] 8-byte key sequence: {key_bytes.hex()}')
print(f'[*] as ASCII: {key_bytes}')

# Then bytes 8 and 9 (rsp+0x28, rsp+0x29):
# mov byte ptr [rsp+0x28], al  where al = r9d XOR 0x3e, r9d = 0x5a -> al = 0x5a^0x3e = 0x64 = 'd'
# mov byte ptr [rsp+0x29], r9b  where r9d XOR 0x60 -> 0x5a^0x60 = 0x3a = ':'
r9d = 0x5a
byte8 = r9d ^ 0x3e  # eax = r9d; xor eax, 0x3e
byte9 = r9d ^ 0x60  # xor r9d, 0x60
print(f'[*] byte 8: 0x{byte8:02x} = {chr(byte8)!r}')
print(f'[*] byte 9: 0x{byte9:02x} = {chr(byte9)!r}')
print(f'[*] Full 10-byte expected: {key_bytes + bytes([byte8, byte9])}')
print(f'[*] Full 10-byte as ASCII: {"".join(chr(b) if 32 <= b < 127 else "?" for b in list(key_bytes) + [byte8, byte9])}')
