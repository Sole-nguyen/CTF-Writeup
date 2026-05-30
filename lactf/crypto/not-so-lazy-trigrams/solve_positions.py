#!/usr/bin/env python3
"""
Since the cipher uses separate shuffles for each position (i, j, k),
we can attack each position independently using frequency analysis.
"""
import re
from collections import Counter
import random

with open('ct.txt', 'r') as f:
    ct = f.read()

clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += 'x' * (3 - len(clean_ct) % 3)

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# Separate by position
pos1_ct = [t[0] for t in ct_trigrams]
pos2_ct = [t[1] for t in ct_trigrams]
pos3_ct = [t[2] for t in ct_trigrams]

# English letter frequencies (from most to least common)
eng_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

# Get frequency for each position
c1 = Counter(pos1_ct)
c2 = Counter(pos2_ct)
c3 = Counter(pos3_ct)

# Create initial mappings based on frequency
map1 = {}
map2 = {}
map3 = {}

# Sort ciphertext chars by frequency
ct1_sorted = [ch for ch, cnt in c1.most_common()]
ct2_sorted = [ch for ch, cnt in c2.most_common()]
ct3_sorted = [ch for ch, cnt in c3.most_common()]

# Initial mapping: most frequent cipher -> most frequent English
for i, ch_ct in enumerate(ct1_sorted):
    if i < len(eng_freq):
        map1[ch_ct] = eng_freq[i]

for i, ch_ct in enumerate(ct2_sorted):
    if i < len(eng_freq):
        map2[ch_ct] = eng_freq[i]

for i, ch_ct in enumerate(ct3_sorted):
    if i < len(eng_freq):
        map3[ch_ct] = eng_freq[i]

def decrypt_with_pos_maps(trigs, m1, m2, m3):
    result = ''
    for t in trigs:
        result += m1.get(t[0], '?') + m2.get(t[1], '?') + m3.get(t[2], '?')
    return result

def score(text):
    s = 0
    # Common words
    s += text.count(' the ') * 20
    s += text.count(' and ') * 15
    s += text.count(' of ') * 12
    s += text.count(' to ') * 12
    s += text.count(' in ') * 10
    s += text.count(' a ') * 10
    s += text.count(' is ') * 8
    s += text.count(' it ') * 8
    s += text.count(' for ') * 8
    s += text.count(' that ') * 8
    s += text.count(' with ') * 7
    s += text.count(' as ') * 7
    s += text.count(' be ') * 6
    s += text.count(' on ') * 6
    s += text.count('ing ') * 10
    s += text.count('tion') * 10
    s += text.count('ment') * 5
    s += text.count('ness') * 5
    s += text.count('lactf{') * 100000
    
    # Penalize
    s -= text.count('xxx') * 30
    s -= text.count('qqq') * 30
    s -= text.count('zzz') * 30
    
    return s

# Hill climbing on each position mapping
best_m1, best_m2, best_m3 = map1.copy(), map2.copy(), map3.copy()
best_score = score(decrypt_with_pos_maps(ct_trigrams, best_m1, best_m2, best_m3))

print(f"Initial score: {best_score}")

for iteration in range(100000):
    # Randomly choose which position to modify
    pos = random.choice([1, 2, 3])
    
    if pos == 1:
        new_m1 = best_m1.copy()
        k1, k2 = random.sample(list(new_m1.keys()), 2)
        new_m1[k1], new_m1[k2] = new_m1[k2], new_m1[k1]
        new_m2, new_m3 = best_m2, best_m3
    elif pos == 2:
        new_m2 = best_m2.copy()
        k1, k2 = random.sample(list(new_m2.keys()), 2)
        new_m2[k1], new_m2[k2] = new_m2[k2], new_m2[k1]
        new_m1, new_m3 = best_m1, best_m3
    else:
        new_m3 = best_m3.copy()
        k1, k2 = random.sample(list(new_m3.keys()), 2)
        new_m3[k1], new_m3[k2] = new_m3[k2], new_m3[k1]
        new_m1, new_m2 = best_m1, best_m2
    
    new_score = score(decrypt_with_pos_maps(ct_trigrams, new_m1, new_m2, new_m3))
    
    if new_score > best_score:
        best_m1, best_m2, best_m3 = new_m1, new_m2, new_m3
        best_score = new_score
        if iteration % 5000 == 0:
            print(f"Iter {iteration}: score = {best_score}")
        if best_score > 5000:  # Likely found good solution
            print(f"Good score at iteration {iteration}: {best_score}")
            break

result = decrypt_with_pos_maps(ct_trigrams, best_m1, best_m2, best_m3)
print("\n" + "="*80)
print("Decrypted text:")
print("="*80)
print(result)

if 'lactf{' in result:
    start = result.find('lactf{')
    end = result.find('}', start)
    print("\n" + "="*80)
    print(f"FLAG: {result[start:end+1]}")
    print("="*80)
