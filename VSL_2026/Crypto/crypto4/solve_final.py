#!/usr/bin/env python3
import socket, hashlib
from functools import lru_cache

@lru_cache(maxsize=5000000)
def _qfm(x, y, bw=512):
    if x == 0 or y == 0: return 0
    if x == 1: return y
    if y == 1: return x
    bw >>= 1
    hx, lx = x >> bw, x & (1 << bw) - 1
    hy, ly = y >> bw, y & (1 << bw) - 1
    lp = _qfm(lx, ly, bw)
    hp = _qfm(hx, hy, bw)
    cs = _qfm(hx ^ lx, hy ^ ly, bw) ^ lp
    ft = _qfm(1 << (bw - 1), hp, bw) ^ lp
    return cs << bw | ft

class QN:
    def __init__(self, e): self.essence = e
    def __mul__(self, o): return QN(_qfm(self.essence, o.essence))
    def __pow__(self, exp):
        base, result = self, QN(1)
        while exp > 0:
            if exp % 2 == 1: result = result * base
            base *= base
            exp >>= 1
        return result

def solve_pow(prefix):
    for i in range(10000000):
        if hashlib.sha256((prefix + str(i)).encode()).hexdigest().startswith('0000'):
            return str(i)

def solve(mp_val, dl_val):
    m = QN(mp_val)
    print('[*] Computing powers 0-2047...')
    pows = [(m ** i).essence for i in range(2048)]
    
    print('[*] Building 2-combo map...')
    two_map = {}
    for i in range(2048):
        if i % 400 == 0:
            print(f'    {i}/2047')
        for j in range(i, 2048):
            val = pows[i] ^ pows[j]
            if val not in two_map:
                two_map[val] = (i, j)
    
    print(f'[*] Map size: {len(two_map)}')
    print('[*] Searching...')
    
    for val1, (i1, i2) in two_map.items():
        target = dl_val ^ val1
        if target in two_map:
            i3, i4 = two_map[target]
            print(f'[*] FOUND: [{i1}, {i2}, {i3}, {i4}]')
            return [i1, i2, i3, i4]
    
    # Try 3-spell
    print('[*] Trying 3-spell...')
    for i in range(2048):
        if i % 400 == 0:
            print(f'    {i}/2047')
        target = dl_val ^ pows[i]
        if target in two_map:
            j, k = two_map[target]
            print(f'[*] FOUND 3-spell: [{i}, {j}, {k}]')
            return [i, j, k]
    
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
print(f'[*] Prefix: {prefix}')

sol = solve_pow(prefix)
print(f'[*] PoW: {sol}')
s.sendall((sol + '\n').encode())

data = b''
while b'Spell Intensity>' not in data:
    data += s.recv(4096)
data = data.decode()
print(data)

mp = int([l for l in data.split('\n') if 'Magic Power:' in l][0].split(':')[1])
dl = int([l for l in data.split('\n') if 'Life Force:' in l][0].split(':')[1])

print(f'[*] Solving...')
spells = solve(mp, dl)

if spells:
    print(f'[*] Solution: {spells}')
    while len(spells) < 4:
        spells.append(0)
    for sp in spells[:4]:
        s.sendall((str(sp) + '\n').encode())
        print(s.recv(4096).decode())
    
    s.settimeout(2)
    try:
        print(s.recv(4096).decode())
    except:
        pass
else:
    print('[!] Failed')

s.close()
