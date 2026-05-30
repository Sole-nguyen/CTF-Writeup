#!/usr/bin/env python3
import socket, hashlib, sys, random
from functools import lru_cache

@lru_cache(maxsize=20000000)
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

def solve_smart(mp_val, dl_val):
    """Try a smarter approach - maybe there's a pattern or specific values work"""
    m = QN(mp_val)
    
    # Strategy 1: Try 4096 with optimized search
    print('[*] Computing 4096 powers...', file=sys.stderr)
    pows = [(m ** i).essence for i in range(4096)]
    
    # Use dict comprehension for faster map building
    print('[*] Building map (optimized)...', file=sys.stderr)
    two_map = {pows[i] ^ pows[j]: (i, j) 
               for i in range(4096) 
               for j in range(i, 4096)}
    
    print(f'[*] Map: {len(two_map)} entries', file=sys.stderr)
    
    # Search
    print('[*] Searching 4-spell...', file=sys.stderr)
    for val1, (i1, i2) in two_map.items():
        target = dl_val ^ val1
        if target in two_map:
            i3, i4 = two_map[target]
            return [i1, i2, i3, i4]
    
    # 3-spell
    print('[*] Searching 3-spell...', file=sys.stderr)
    for i in range(4096):
        target = dl_val ^ pows[i]
        if target in two_map:
            j, k = two_map[target]
            return [i, j, k]
    
    # Strategy 2: Try specific large values based on field theory
    print('[*] Trying special exponents...', file=sys.stderr)
    special = []
    
    # Fermat numbers and Mersenne numbers
    for k in range(2, 20):
        special.extend([2**k - 1, 2**k, 2**k + 1])
    
    # Sparse high values
    for i in range(5000, 100000, 100):
        special.append(i)
    
    # Random sample in very high range
    for _ in range(100):
        special.append(random.randint(100000, 1000000))
    
    special = sorted(set(special))
    print(f'[*] Computing {len(special)} special powers...', file=sys.stderr)
    
    special_pows = {e: (m ** e).essence for e in special}
    
    # Combined search: 4096 regular + special
    all_exps = list(range(4096)) + special
    all_pows = {**{i: pows[i] for i in range(4096)}, **special_pows}
    
    print('[*] Building combined 2-map...', file=sys.stderr)
    combined_map = {}
    for e1 in all_exps:
        for e2 in all_exps:
            if e2 >= e1:
                val = all_pows[e1] ^ all_pows[e2]
                if val not in combined_map:
                    combined_map[val] = (e1, e2)
    
    print(f'[*] Combined map: {len(combined_map)} entries', file=sys.stderr)
    print('[*] Searching combined...', file=sys.stderr)
    
    for val1, (i1, i2) in combined_map.items():
        target = dl_val ^ val1
        if target in combined_map:
            i3, i4 = combined_map[target]
            return [i1, i2, i3, i4]
    
    # 3-spell with combined
    for e in all_exps:
        target = dl_val ^ all_pows[e]
        if target in combined_map:
            j, k = combined_map[target]
            return [e, j, k]
    
    return None

# Main
print('[*] Connecting...', file=sys.stderr)
s = socket.socket()
s.connect(('61.14.233.78', 6669))

data = b''
while b'Your proof:' not in data:
    data += s.recv(4096)
data = data.decode()

prefix = [l for l in data.split('\n') if 'Challenge:' in l][0].split()[1]
print(f'[*] Prefix: {prefix}', file=sys.stderr)

sol = solve_pow(prefix)
print(f'[*] PoW: {sol}', file=sys.stderr)
s.sendall((sol + '\n').encode())

data = b''
while b'Spell Intensity>' not in data:
    data += s.recv(4096)
data = data.decode()

mp = int([l for l in data.split('\n') if 'Magic Power:' in l][0].split(':')[1])
dl = int([l for l in data.split('\n') if 'Life Force:' in l][0].split(':')[1])

print(f'[*] Solving...', file=sys.stderr)
spells = solve_smart(mp, dl)

if spells:
    print(f'[*] Solution: {spells}', file=sys.stderr)
    while len(spells) < 4:
        spells.append(0)
    for sp in spells[:4]:
        s.sendall((str(sp) + '\n').encode())
        resp = s.recv(4096).decode()
        print(resp[:200], file=sys.stderr)
    
    s.settimeout(3)
    try:
        final = s.recv(4096).decode()
        print(final)
        if 'VSL{' in final:
            flag_start = final.index('VSL{')
            flag_end = final.index('}', flag_start) + 1
            flag = final[flag_start:flag_end]
            print(f'\n=== FLAG ===\n{flag}\n============')
    except:
        pass
else:
    print('[!] No solution', file=sys.stderr)

s.close()
