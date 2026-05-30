import struct

with open('oracle','rb') as f:
    data = f.read()

# Compute hash of chk section
chk_start = 0x4340
chk_end = 0x457e
chk_data = data[chk_start:chk_end]
print(f'Hashing chk section: {hex(chk_start)} to {hex(chk_end)} ({len(chk_data)} bytes)')

ebx = 0xc0def1ab
for byte in chk_data:
    eax = (byte ^ ebx) & 0xffffffff
    eax = (eax * 0x5bd1e995) & 0xffffffff
    ebx_shifted = (eax >> 0xf) & 0xffffffff
    ebx = (ebx_shifted ^ eax) & 0xffffffff
    
print(f'Hash: 0x{ebx:08x}')

table1 = [struct.unpack_from('<I', data, 0x7000 + i*4)[0] for i in range(4)]
table2 = [struct.unpack_from('<I', data, 0x7010 + i*4)[0] for i in range(4)]
print('Table1:', [hex(k) for k in table1])
print('Table2:', [hex(k) for k in table2])

key = [(table1[i] ^ ebx ^ table2[i]) & 0xffffffff for i in range(4)]
print('XTEA key (normal):', [hex(k) for k in key])

key_piped = key.copy()
key_piped[0] ^= 0xdeadbeef
print('XTEA key (piped):', [hex(k) for k in key_piped])

# XTEA decrypt feed.bin
def xtea_decrypt_block(block, key):
    """Decrypt 8 bytes (2 uint32s) with XTEA"""
    v0, v1 = struct.unpack('<II', block)
    
    delta = 0x9e3779b9
    num_rounds = 32
    total_sum = (delta * num_rounds) & 0xffffffff
    
    s = total_sum
    for _ in range(num_rounds):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & 0xffffffff
        s = (s - delta) & 0xffffffff
    
    return struct.pack('<II', v0, v1)

def xtea_decrypt(ciphertext, key):
    result = b''
    for i in range(0, len(ciphertext), 8):
        result += xtea_decrypt_block(ciphertext[i:i+8], key)
    return result

with open('feed.bin','rb') as f:
    feed = f.read()

print(f'\nFeed size: {len(feed)} bytes')

# Try both keys
for k, kname in [(key, 'normal'), (key_piped, 'piped')]:
    decrypted = xtea_decrypt(feed, k)
    print(f'\n=== Decrypted with {kname} key ===')
    print('First 64 bytes hex:', decrypted[:64].hex())
    printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in decrypted[:128])
    print('First 128 bytes ASCII:', printable)
    
    # Look for interesting patterns
    import re
    strings = re.findall(b'[ -~]{4,}', decrypted)
    if strings:
        print('Strings found:')
        for s in strings[:20]:
            print(' ', s)
