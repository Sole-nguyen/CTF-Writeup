#!/usr/bin/env python3
import socket
import hashlib
from functools import lru_cache

@lru_cache(maxsize=200000)
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
    
    print("[*] Testing candidate exponents...")
    # Expand search space significantly
    candidates = list(range(500))  # 0-499
    # Add special values
    for k in range(3, 20):
        candidates.extend([2**k - 1, 2**k, 2**k + 1])
    
    # Add more values up to 2000
    candidates.extend(range(500, 1000, 2))  # Every other value 500-1000
    
    powers = {}
    for i in sorted(set(candidates)):
        powers[i] = (mp ** i).essence
    
    print(f"[*] Computed {len(powers)} powers")
    
    # Build hash map for meet-in-the-middle
    two_map = {}
    exps = list(powers.keys())
    for i, e1 in enumerate(exps):
        if i % 50 == 0:
            print(f"    Building map: {i}/{len(exps)}")
        for e2 in exps:
            val = powers[e1] ^ powers[e2]
            if val not in two_map:
                two_map[val] = []
            two_map[val].append((e1, e2))
    
    print(f"[*] Created map with {len(two_map)} entries")
    print(f"[*] Searching for 4-spell solution...")
    
    # Search for match
    for val1, pairs1 in two_map.items():
        target = dl_val ^ val1
        if target in two_map:
            p1, p2 = pairs1[0], two_map[target][0]
            result = [p1[0], p1[1], p2[0], p2[1]]
            print(f"[*] Found: {result}")
            return result
    
    # 3-spell
    print("[*] Trying 3-spell...")
    for e in exps:
        target = dl_val ^ powers[e]
        if target in two_map:
            p = two_map[target][0]
            result = [e, p[0], p[1]]
            print(f"[*] Found 3-spell: {result}")
            return result
    
    # 2-spell
    if dl_val in two_map:
        p = two_map[dl_val][0]
        result = [p[0], p[1]]
        print(f"[*] Found 2-spell: {result}")
        return result
    
    # 1-spell
    for e, v in powers.items():
        if v == dl_val:
            print(f"[*] Found 1-spell: [{e}]")
            return [e]
    
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

print(f"[*] MP: {mp}")
print(f"[*] DL: {dl}")

spells = solve_dragon(mp, dl)
if spells:
    while len(spells) < 4:
        spells.append(0)
    for sp in spells[:4]:
        s.sendall((str(sp) + '\n').encode())
        print(s.recv(4096).decode())
else:
    print("[!] Failed")

s.close()
