#!/usr/bin/env python3
import re
from collections import Counter
import random

with open('ct.txt', 'r') as f:
    ct = f.read()

clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += 'x' * (3 - len(clean_ct) % 3)

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

def decrypt(trigs, mapping):
    return ''.join([mapping.get(t, '...') for t in trigs])

def score(text):
    s = 0
    s += text.count(' the ') * 20
    s += text.count(' and ') * 15
    s += text.count('ing ') * 10
    s += text.count(' of ') * 10
    s += text.count(' to ') * 10
    s += text.count(' in ') * 10
    s += text.count(' a ') * 8
    s += text.count('tion') * 8
    s += text.count(' for ') * 7
    s += text.count(' is ') * 7
    s += text.count(' that ') * 7
    s += text.count(' it ') * 6
    s += text.count(' as ') * 6
    s += text.count(' with ') * 6
    s += text.count(' be ') * 5
    s += text.count('lactf{') * 10000
    
    # Penalize weird patterns
    s -= text.count('xxx') * 20
    s -= text.count('qqq') * 20
    return s

# Initialize with frequency mapping
freq = Counter(ct_trigrams)
common_ct = [t for t, c in freq.most_common()]
common_en = ['the', 'and', 'ing', 'ent', 'ion', 'tio', 'for', 'ter', 'hat', 'tha', 
             'ere', 'ate', 'res', 'ver', 'his', 'her', 'all', 'was', 'not', 'are',
             'but', 'can', 'had', 'you', 'one', 'our', 'out', 'who', 'has', 'now']

# Generate all possible trigrams
all_trig = [chr(i)+chr(j)+chr(k) for i in range(97,123) for j in range(97,123) for k in range(97,123)]
random.shuffle(all_trig)

mapping = {}
for i in range(min(len(common_ct), len(common_en))):
    mapping[common_ct[i]] = common_en[i]

# Fill remaining
used = set(mapping.values())
j = 0
for ct in common_ct:
    if ct not in mapping:
        while all_trig[j] in used:
            j += 1
        mapping[ct] = all_trig[j]
        used.add(all_trig[j])
        j += 1

# Hill climbing
best_map = mapping.copy()
best_score = score(decrypt(ct_trigrams, best_map))

print(f"Initial score: {best_score}")

for iteration in range(20000):
    # Try swapping two mappings
    new_map = best_map.copy()
    k1, k2 = random.sample(list(new_map.keys()), 2)
    new_map[k1], new_map[k2] = new_map[k2], new_map[k1]
    
    new_score = score(decrypt(ct_trigrams, new_map))
    
    if new_score > best_score:
        best_map = new_map
        best_score = new_score
        if iteration % 1000 == 0:
            print(f"Iter {iteration}: score = {best_score}")
            dec = decrypt(ct_trigrams, best_map)
            if 'lactf{' in dec:
                print("FOUND FLAG!")
                print(dec)
                break

result = decrypt(ct_trigrams, best_map)
print("\n" + "="*80)
print(result)

if 'lactf{' in result:
    start = result.find('lactf{')
    end = result.find('}', start)
    print("\n" + "="*80)
    print(f"FLAG: {result[start:end+1]}")
    print("="*80)
