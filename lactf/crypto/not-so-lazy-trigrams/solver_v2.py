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

# Load common English words
COMMON_2 = set(['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am'])
COMMON_3 = set(['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'who', 'oil', 'its', 'now', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'see', 'way', 'who', 'boy', 'did', 'may', 'old', 'too', 'say', 'she', 'use'])

def decrypt(trigs, mapping):
    return ''.join([mapping.get(t, '...') for t in trigs])

def score(text):
    s = 0
    words = text.split()
    for w in words:
        if w in COMMON_2:
            s += 10
        if w in COMMON_3:
            s += 15
    
    # Common trigrams
    s += text.count('the') * 5
    s += text.count('and') * 4
    s += text.count('ing') * 4
    s += text.count('ion') * 3
    s += text.count('tio') * 3
    s += text.count(' of ') * 8
    s += text.count(' to ') * 8
    s += text.count(' in ') * 7
    s += text.count(' is ') * 6
    s += text.count(' it ') * 6
    s += text.count(' for ') * 6
    s += text.count(' that ') * 8
    s += text.count(' with ') * 7
    s += text.count(' this ') * 7
    s += text.count('lactf{') * 50000
    
    # Penalize
    s -= text.count('xxx') * 50
    s -= text.count('qqq') * 50
    s -= text.count('jjj') * 30
    s -= text.count('zzz') * 30
    
    return s

# Initialize
freq = Counter(ct_trigrams)
common_ct = [t for t, c in freq.most_common()]
common_en = ['the', 'and', 'ing', 'tion', 'for', 'ter', 'hat', 'tha', 'ere', 'ate', 
             'ent', 'ion', 'tio', 'res', 'ver', 'his', 'her', 'all', 'was', 'not',
             'are', 'but', 'had', 'can', 'you', 'one', 'our', 'out', 'who', 'has']

all_trig = [chr(i)+chr(j)+chr(k) for i in range(97,123) for j in range(97,123) for k in range(97,123)]
random.shuffle(all_trig)

mapping = {}
for i in range(min(len(common_ct), len(common_en))):
    mapping[common_ct[i]] = common_en[i]

used = set(mapping.values())
j = 0
for ct in common_ct:
    if ct not in mapping:
        while all_trig[j] in used:
            j += 1
        mapping[ct] = all_trig[j]
        used.add(all_trig[j])
        j += 1

best_map = mapping.copy()
best_score = score(decrypt(ct_trigrams, best_map))
print(f"Initial: {best_score}")

# Run longer
for it in range(50000):
    new_map = best_map.copy()
    k1, k2 = random.sample(list(new_map.keys()), 2)
    new_map[k1], new_map[k2] = new_map[k2], new_map[k1]
    
    new_score = score(decrypt(ct_trigrams, new_map))
    
    if new_score > best_score:
        best_map = new_map
        best_score = new_score
        if it % 2500 == 0:
            print(f"{it}: {best_score}")
    
    if best_score > 10000:  # Found flag likely
        break

result = decrypt(ct_trigrams, best_map)
print("\n" + "="*80)
print(result[:500])
print("\n...")
print(result[-200:])

if 'lactf{' in result:
    start = result.find('lactf{')
    end = result.find('}', start)
    print("\n" + "="*80)
    print(f"FLAG: {result[start:end+1]}")
    print("="*80)
else:
    print("\nNo flag found, continuing search...")
