#!/usr/bin/env python3
import socket
import hashlib
from functools import lru_cache

@lru_cache(maxsize=500000)
def _quantum_field_multiply(val_x, val_y, bit_width=512):
    if val_x == 0 or val_y == 0:
        return 0
    if val_x == 1:
        return val_y
    if val_y == 1:
        return val_x
    bit_width >>= 1
    high_x, low_x = val_x >> bit_width, val_x & (1 << bit_width) - 1
    high_y, low_y = val_y >> bit_width, val_y & (1 << bit_width) - 1
    low_product = _quantum_field_multiply(low_x, low_y, bit_width)
    high_product = _quantum_field_multiply(high_x, high_y, bit_width)
    cross_sum = _quantum_field_multiply(high_x ^ low_x, high_y ^ low_y, bit_width) ^ low_product
    fermat_term = _quantum_field_multiply(1 << (bit_width - 1), high_product, bit_width) ^ low_product
    return cross_sum << bit_width | fermat_term

class QuantumNimber:
    def __init__(self, essence):
        self.essence = essence
    def __mul__(self, other):
        return QuantumNimber(_quantum_field_multiply(self.essence, other.essence))
    def __pow__(self, exponent):
        base, result = self, QuantumNimber(1)
        while exponent > 0:
            if exponent % 2 == 1:
                result = result * base
            base *= base
            exponent //= 2
        return result

def solve_pow(prefix):
    for i in range(10000000):
        if hashlib.sha256((prefix + str(i)).encode()).hexdigest().startswith('0000'):
            return str(i)

def solve_dragon(mp_val, dl_val):
    mp = QuantumNimber(mp_val)
    
    print("[*] Computing powers 0-255...")
    powers = [(mp ** i).essence for i in range(256)]
    
    print("[*] 4-nested search 0-31...")
    for i1 in range(32):
        if i1 % 4 == 0:
            print(f"    i1={i1}/31")
        for i2 in range(32):
            for i3 in range(32):
                for i4 in range(32):
                    if powers[i1] ^ powers[i2] ^ powers[i3] ^ powers[i4] == dl_val:
                        return [i1, i2, i3, i4]
    
    print("[*] 4-nested search 0-63 (skip inner if found above)...")
    for i1 in range(64):
        if i1 % 8 == 0:
            print(f"    i1={i1}/63")
        for i2 in range(64):
            for i3 in range(64):
                for i4 in range(64):
                    if powers[i1] ^ powers[i2] ^ powers[i3] ^ powers[i4] == dl_val:
                        return [i1, i2, i3, i4]
    
    print("[*] Meet-in-middle with 0-255...")
    # Build all 2-combos
    two_map = {}
    for i in range(256):
        for j in range(i, 256):
            val = powers[i] ^ powers[j]
            if val not in two_map:
                two_map[val] = (i, j)
    
    # Search
    for val1, (i1, i2) in two_map.items():
        target = dl_val ^ val1
        if target in two_map:
            i3, i4 = two_map[target]
            return [i1, i2, i3, i4]
    
    # 3-spell
    for i in range(256):
        target = dl_val ^ powers[i]
        if target in two_map:
            i2, i3 = two_map[target]
            return [i, i2, i3]
    
    # 2-spell
    if dl_val in two_map:
        i1, i2 = two_map[dl_val]
        return [i1, i2]
    
    # 1-spell
    if dl_val in powers:
        return [powers.index(dl_val)]
    
    return None

# Main
s = socket.socket()
s.connect(('61.14.233.78', 6669))

data = b''
while b'Your proof:' not in data:
    data += s.recv(4096)
data = data.decode()
print(data)

prefix = [l for l in data.split('\n') if 'Challenge:' in l][0].split()[1]
print(f"[*] Prefix: {prefix}")

sol = solve_pow(prefix)
print(f"[*] PoW: {sol}")
s.sendall((sol + '\n').encode())

data = b''
while b'Spell Intensity>' not in data:
    data += s.recv(4096)
data = data.decode()
print(data)

mp = int([l for l in data.split('\n') if 'Magic Power:' in l][0].split(':')[1])
dl = int([l for l in data.split('\n') if 'Life Force:' in l][0].split(':')[1])

print(f"[*] Solving...")

spells = solve_dragon(mp, dl)
if spells:
    print(f"[*] Solution: {spells}")
    while len(spells) < 4:
        spells.append(0)
    for sp in spells[:4]:
        s.sendall((str(sp) + '\n').encode())
        resp = s.recv(4096).decode()
        print(resp)
    
    # Get flag
    s.settimeout(2)
    try:
        final = s.recv(4096).decode()
        print(final)
    except:
        pass
else:
    print("[!] Failed")

s.close()
