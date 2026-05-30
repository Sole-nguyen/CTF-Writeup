#!/usr/bin/env python3
import re, random, math
from collections import Counter

with open('ct.txt') as f:
    ct = f.read()

clean = re.sub(r'[^a-zA-Z]', '', ct).lower()
clean += 'x' * ((3 - len(clean) % 3) % 3)
trigs = [clean[i:i+3] for i in range(0, len(clean), 3)]

p1 = [t[0] for t in trigs]
p2 = [t[1] for t in trigs]
p3 = [t[2] for t in trigs]

freq_en = 'etaoinshrdlcumwfgypbvkjxqz'
c1, c2, c3 = Counter(p1), Counter(p2), Counter(p3)

ct1 = [c for c, _ in c1.most_common()]
ct2 = [c for c, _ in c2.most_common()]
ct3 = [c for c, _ in c3.most_common()]

m1 = {ct1[i]: freq_en[i] for i in range(len(ct1))}
m2 = {ct2[i]: freq_en[i] for i in range(len(ct2))}
m3 = {ct3[i]: freq_en[i] for i in range(len(ct3))}

# Constraint
m1['n'] = 'l'
m2['j'] = 'a'
m3['l'] = 'c'

def dec(m1, m2, m3):
    return ''.join([m1[t[0]] + m2[t[1]] + m3[t[2]] for t in trigs])

def sc(txt):
    s = txt.count(' the ') * 200
    s += txt.count(' and ') * 150
    s += txt.count(' of ') * 120
    s += txt.count(' to ') * 120
    s += txt.count(' in ') * 100
    s += txt.count(' a ') * 100
    s += txt.count(' is ') * 80
    s += txt.count(' for ') * 80
    s += txt.count(' that ') * 80
    s += txt.count(' with ') * 70
    s += txt.count(' it ') * 70
    s += txt.count(' as ') * 70
    s += txt.count(' on ') * 60
    s += txt.count('ing ') * 100
    s += txt.count('tion') * 100
    s += txt.count('lactf{') * 9999999
    s -= txt.count('xxx') * 200
    s -= txt.count('qqq') * 200
    s -= txt.count('  ') * 100
    return s

best = (m1.copy(), m2.copy(), m3.copy())
curr = best
bs = sc(dec(*best))
cs = bs
temp = 500.0
cool = 0.99995

print(f"Init: {bs}")

for it in range(1000000):
    pos = random.choice([0, 1, 2])
    new = list(curr)
    
    fixed = ['n', 'j', 'l'][pos]
    keys = [k for k in new[pos].keys() if k != fixed]
    if len(keys) < 2:
        continue
        
    k1, k2 = random.sample(keys, 2)
    new[pos] = new[pos].copy()
    new[pos][k1], new[pos][k2] = new[pos][k2], new[pos][k1]
    
    ns = sc(dec(*new))
    delta = ns - cs
    
    if delta > 0 or (temp > 0.1 and random.random() < math.exp(delta / temp)):
        curr = tuple(new)
        cs = ns
        
        if cs > bs:
            best = curr
            bs = cs
            if it % 50000 == 0:
                print(f"{it}: {bs:.0f}")
    
    temp *= cool
    
    if bs > 500000:
        print(f"FOUND at {it}: {bs:.0f}")
        break

result = dec(*best)
print("="*80)
print(result)

if 'lactf{' in result:
    i = result.find('lactf{')
    j = result.find('}', i)
    print("="*80)
    print(f"FLAG: {result[i:j+1]}")
