#!/usr/bin/env python3
"""
Key insight: The cipher uses separate independent shuffles for each position.
If njl -> lac, then:
- In position 0: 'n' maps to 'l' (position 11 in alphabet)
- In position 1: 'j' maps to 'a' (position 0 in alphabet)  
- In position 2: 'l' maps to 'c' (position 2 in alphabet)

But we need more known plaintexts to deduce the full shuffles.
Let's use frequency analysis on each position independently with simulated annealing.
"""
import re
from collections import Counter
import random
import math

with open('ct.txt', 'r') as f:
    ct = f.read()

clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += 'x' * (3 - len(clean_ct) % 3)

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# Constraint: njl -> lac
# This gives us partial information about each position's mapping

pos1_ct = [t[0] for t in ct_trigrams]
pos2_ct = [t[1] for t in ct_trigrams]
pos3_ct = [t[2] for t in ct_trigrams]

# English letter frequencies
eng_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

c1, c2, c3 = Counter(pos1_ct), Counter(pos2_ct), Counter(pos3_ct)

ct1_sorted = [ch for ch, cnt in c1.most_common()]
ct2_sorted = [ch for ch, cnt in c2.most_common()]
ct3_sorted = [ch for ch, cnt in c3.most_common()]

# Initialize mappings
map1 = {ct1_sorted[i]: eng_freq[i] for i in range(min(len(ct1_sorted), len(eng_freq)))}
map2 = {ct2_sorted[i]: eng_freq[i] for i in range(min(len(ct2_sorted), len(eng_freq)))}
map3 = {ct3_sorted[i]: eng_freq[i] for i in range(min(len(ct3_sorted), len(eng_freq)))}

# Apply constraints from known plaintext: njl -> lac
map1['n'] = 'l'
map2['j'] = 'a'
map3['l'] = 'c'

def decrypt(trigs, m1, m2, m3):
    return ''.join([m1.get(t[0], '?') + m2.get(t[1], '?') + m3.get(t[2], '?') for t in trigs])

def score(text):
    s = 0
    # Heavy scoring for common patterns
    s += text.count(' the ') * 100
    s += text.count(' and ') * 80
    s += text.count(' of ') * 70
    s += text.count(' to ') * 70
    s += text.count(' in ') * 60
    s += text.count(' a ') * 60
    s += text.count(' is ') * 50
    s += text.count(' for ') * 50
    s += text.count(' that ') * 50
    s += text.count(' with ') * 45
    s += text.count(' it ') * 40
    s += text.count(' as ') * 40
    s += text.count(' be ') * 35
    s += text.count(' on ') * 35
    s += text.count(' at ') * 35
    s += text.count(' this ') * 45
    s += text.count(' from ') * 40
    s += text.count('ing ') * 60
    s += text.count('tion') * 60
    s += text.count('ness') * 30
    s += text.count('ment') * 30
    s += text.count(' are ') * 40
    s += text.count(' was ') * 40
    s += text.count(' have ') * 35
    s += text.count('lactf{') * 5000000
    
    # Penalize
    s -= text.count('xxx') * 100
    s -= text.count('qqq') * 100
    s -= text.count('zzz') * 100
    s -= text.count('  ') * 50
    
    return s

# Simulated annealing
temp = 200.0
cooling = 0.99992

best = (map1.copy(), map2.copy(), map3.copy())
curr = (map1.copy(), map2.copy(), map3.copy())
best_score = score(decrypt(ct_trigrams, *best))
curr_score = best_score

print(f"Initial: {best_score}")

for it in range(500000):
    pos = random.choice([1, 2, 3])
    
    new = list(curr)
    # Don't modify the constrained mappings
    if pos == 1:
        new_m = new[0].copy()
        keys = [k for k in new_m.keys() if k != 'n']  # Don't swap 'n'
        if len(keys) >= 2:
            k1, k2 = random.sample(keys, 2)
            new_m[k1], new_m[k2] = new_m[k2], new_m[k1]
        new[0] = new_m
    elif pos == 2:
        new_m = new[1].copy()
        keys = [k for k in new_m.keys() if k != 'j']  # Don't swap 'j'
        if len(keys) >= 2:
            k1, k2 = random.sample(keys, 2)
            new_m[k1], new_m[k2] = new_m[k2], new_m[k1]
        new[1] = new_m
    else:
        new_m = new[2].copy()
        keys = [k for k in new_m.keys() if k != 'l']  # Don't swap 'l'
        if len(keys) >= 2:
            k1, k2 = random.sample(keys, 2)
            new_m[k1], new_m[k2] = new_m[k2], new_m[k1]
        new[2] = new_m
    
    new_score = score(decrypt(ct_trigrams, *new))
    
    delta = new_score - curr_score
    if delta > 0 or (temp > 0.01 and random.random() < math.exp(delta / temp)):
        curr = tuple(new)
        curr_score = new_score
        
        if curr_score > best_score:
            best = curr
            best_score = curr_score
            if it % 25000 == 0:
                print(f"{it}: {best_score:.0f}")
    
    temp *= cooling
    
    if best_score > 100000:
        print(f"Found great solution at {it}: {best_score:.0f}")
        break

result = decrypt(ct_trigrams, *best)
print("\n" + "="*80)
print(result)

if 'lactf{' in result:
    start = result.find('lactf{')
    end = result.find('}', start)
    print("\n" + "="*80)
    print(f"FLAG: {result[start:end+1]}")
    print("="*80)
else:
    print("\nSearching for 'lac' pattern...")
    if 'lac' in result:
        idx = result.find('lac')
        print(f"Found 'lac' at {idx}: ...{result[max(0,idx-20):idx+40]}...")
