#!/usr/bin/env python3
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

pos1_ct = [t[0] for t in ct_trigrams]
pos2_ct = [t[1] for t in ct_trigrams]
pos3_ct = [t[2] for t in ct_trigrams]

eng_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

c1, c2, c3 = Counter(pos1_ct), Counter(pos2_ct), Counter(pos3_ct)

ct1_sorted = [ch for ch, cnt in c1.most_common()]
ct2_sorted = [ch for ch, cnt in c2.most_common()]
ct3_sorted = [ch for ch, cnt in c3.most_common()]

map1 = {ct1_sorted[i]: eng_freq[i] for i in range(min(len(ct1_sorted), len(eng_freq)))}
map2 = {ct2_sorted[i]: eng_freq[i] for i in range(min(len(ct2_sorted), len(eng_freq)))}
map3 = {ct3_sorted[i]: eng_freq[i] for i in range(min(len(ct3_sorted), len(eng_freq)))}

def decrypt_with_pos_maps(trigs, m1, m2, m3):
    return ''.join([m1.get(t[0], '?') + m2.get(t[1], '?') + m3.get(t[2], '?') for t in trigs])

def score(text):
    s = 0
    s += text.count(' the ') * 30
    s += text.count(' and ') * 25
    s += text.count(' of ') * 20
    s += text.count(' to ') * 20
    s += text.count(' in ') * 15
    s += text.count(' a ') * 15
    s += text.count(' is ') * 12
    s += text.count(' for ') * 12
    s += text.count(' that ') * 12
    s += text.count(' with ') * 10
    s += text.count(' it ') * 10
    s += text.count(' as ') * 10
    s += text.count(' be ') * 8
    s += text.count(' on ') * 8
    s += text.count(' at ') * 8
    s += text.count(' this ') * 10
    s += text.count('ing ') * 15
    s += text.count('tion') * 15
    s += text.count('ment') * 8
    s += text.count('ness') * 8
    s += text.count('lactf{') * 500000
    
    # Penalize
    s -= text.count('xxx') * 50
    s -= text.count('qqq') * 50
    s -= text.count('zzz') * 50
    s -= text.count('  ') * 10  # double spaces
    
    return s

# Simulated annealing
temp = 100.0
cooling = 0.9995

best_m1, best_m2, best_m3 = map1.copy(), map2.copy(), map3.copy()
curr_m1, curr_m2, curr_m3 = map1.copy(), map2.copy(), map3.copy()
best_score = score(decrypt_with_pos_maps(ct_trigrams, best_m1, best_m2, best_m3))
curr_score = best_score

print(f"Initial: {best_score}")

for it in range(200000):
    pos = random.choice([1, 2, 3])
    
    if pos == 1:
        new_m1 = curr_m1.copy()
        k1, k2 = random.sample(list(new_m1.keys()), 2)
        new_m1[k1], new_m1[k2] = new_m1[k2], new_m1[k1]
        new_m2, new_m3 = curr_m2, curr_m3
    elif pos == 2:
        new_m2 = curr_m2.copy()
        k1, k2 = random.sample(list(new_m2.keys()), 2)
        new_m2[k1], new_m2[k2] = new_m2[k2], new_m2[k1]
        new_m1, new_m3 = curr_m1, curr_m3
    else:
        new_m3 = curr_m3.copy()
        k1, k2 = random.sample(list(new_m3.keys()), 2)
        new_m3[k1], new_m3[k2] = new_m3[k2], new_m3[k1]
        new_m1, new_m2 = curr_m1, curr_m2
    
    new_score = score(decrypt_with_pos_maps(ct_trigrams, new_m1, new_m2, new_m3))
    
    delta = new_score - curr_score
    if delta > 0 or (temp > 0 and random.random() < math.exp(delta / temp)):
        curr_m1, curr_m2, curr_m3 = new_m1, new_m2, new_m3
        curr_score = new_score
        
        if curr_score > best_score:
            best_m1, best_m2, best_m3 = curr_m1, curr_m2, curr_m3
            best_score = curr_score
            if it % 10000 == 0:
                print(f"{it}: {best_score:.0f}, temp={temp:.4f}")
    
    temp *= cooling
    
    if best_score > 50000:
        print(f"Found at {it}: {best_score:.0f}")
        break

result = decrypt_with_pos_maps(ct_trigrams, best_m1, best_m2, best_m3)
print("\n" + "="*80)
print(result[:600])
print("\n...")
print(result[-300:])

if 'lactf{' in result:
    start = result.find('lactf{')
    end = result.find('}', start)
    print("\n" + "="*80)
    print(f"FLAG: {result[start:end+1]}")
    print("="*80)
