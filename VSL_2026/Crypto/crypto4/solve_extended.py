#!/usr/bin/env python3
import socket, hashlib, sys
from functools import lru_cache

@lru_cache(maxsize=10000000)
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
    
    # Try progressively larger ranges
    for max_exp in [4096, 8192, 16384, 32768, 65536]:
        print(f'[*] Attempting range 0-{max_exp-1}...', file=sys.stderr)
        
        print(f'[*] Computing powers 0-{max_exp-1}...', file=sys.stderr)
        pows = [(m ** i).essence for i in range(max_exp)]
        
        print(f'[*] Building 2-combo map...', file=sys.stderr)
        two_map = {}
        for i in range(max_exp):
            if i % 2000 == 0:
                print(f'    {i}/{max_exp-1}', file=sys.stderr)
            for j in range(i, max_exp):
                val = pows[i] ^ pows[j]
                if val not in two_map:
                    two_map[val] = (i, j)
        
        print(f'[*] Map size: {len(two_map)}', file=sys.stderr)
        print(f'[*] Searching for 4-spell...', file=sys.stderr)
        
        for val1, (i1, i2) in two_map.items():
            target = dl_val ^ val1
            if target in two_map:
                i3, i4 = two_map[target]
                print(f'[*] FOUND 4-spell: [{i1}, {i2}, {i3}, {i4}]', file=sys.stderr)
                return [i1, i2, i3, i4]
        
        # Try 3-spell
        print(f'[*] Trying 3-spell...', file=sys.stderr)
        for i in range(max_exp):
            if i % 2000 == 0:
                print(f'    {i}/{max_exp-1}', file=sys.stderr)
            target = dl_val ^ pows[i]
            if target in two_map:
                j, k = two_map[target]
                print(f'[*] FOUND 3-spell: [{i}, {j}, {k}]', file=sys.stderr)
                return [i, j, k]
        
        # Try 2-spell
        if dl_val in two_map:
            i, j = two_map[dl_val]
            print(f'[*] FOUND 2-spell: [{i}, {j}]', file=sys.stderr)
            return [i, j]
        
        # Try 1-spell
        if dl_val in pows:
            idx = pows.index(dl_val)
            print(f'[*] FOUND 1-spell: [{idx}]', file=sys.stderr)
            return [idx]
        
        print(f'[*] Not found in 0-{max_exp-1}, trying larger range...', file=sys.stderr)
        
        # Clear cache periodically to avoid memory issues
        _qfm.cache_clear()
    
    return None

# Main
print('[*] Connecting...', file=sys.stderr)
s = socket.socket()
s.connect(('61.14.233.78', 6669))

data = b''
while b'Your proof:' not in data:
    data += s.recv(4096)
data = data.decode()
print(data[:300], file=sys.stderr)

prefix = [l for l in data.split('\n') if 'Challenge:' in l][0].split()[1]
print(f'[*] Prefix: {prefix}', file=sys.stderr)

sol = solve_pow(prefix)
print(f'[*] PoW: {sol}', file=sys.stderr)
s.sendall((sol + '\n').encode())

data = b''
while b'Spell Intensity>' not in data:
    data += s.recv(4096)
data = data.decode()
print(data[:300], file=sys.stderr)

mp = int([l for l in data.split('\n') if 'Magic Power:' in l][0].split(':')[1])
dl = int([l for l in data.split('\n') if 'Life Force:' in l][0].split(':')[1])

print(f'[*] MP: {mp}', file=sys.stderr)
print(f'[*] DL: {dl}', file=sys.stderr)

print(f'[*] Starting solve...', file=sys.stderr)
spells = solve(mp, dl)

if spells:
    print(f'[*] Solution: {spells}', file=sys.stderr)
    while len(spells) < 4:
        spells.append(0)
    for sp in spells[:4]:
        s.sendall((str(sp) + '\n').encode())
        resp = s.recv(4096).decode()
        print(resp, file=sys.stderr)
    
    # Get flag
    s.settimeout(3)
    try:
        final = s.recv(4096).decode()
        print(final)
        # Extract flag
        if 'VSL{' in final:
            flag_start = final.index('VSL{')
            flag_end = final.index('}', flag_start) + 1
            flag = final[flag_start:flag_end]
            print(f'\n\n=== FLAG FOUND ===\n{flag}\n==================\n')
    except Exception as e:
        print(f'Error reading final: {e}', file=sys.stderr)
else:
    print('[!] Failed to find solution', file=sys.stderr)

s.close()
