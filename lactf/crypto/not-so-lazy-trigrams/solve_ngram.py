#!/usr/bin/env python3
import re, random, math
from collections import Counter

class NGramScore:
    def __init__(self):
        # More comprehensive trigram scores
        self.floor = -15.0
        # Use reasonable estimates for common trigrams
        common = ['the', 'and', 'ing', 'ion', 'tio', 'ent', 'ati', 'for', 'ter', 'hat',
                  'tha', 'ere', 'ate', 'his', 'con', 'res', 'ver', 'all', 'nth', 'her']
        self.ngrams = {t: -2.0 - i*0.1 for i, t in enumerate(common)}
        
        # Add word bonuses
        self.words = {'the': 50, 'and': 40, 'for': 30, 'that': 30, 'with': 28}
    
    def score(self, text):
        s = 0.0
        # Trigram scores
        for i in range(len(text) - 2):
            s += self.ngrams.get(text[i:i+3], self.floor)
        
        # Word bonuses
        for word, bonus in self.words.items():
            s += text.count(' ' + word + ' ') * bonus
        
        # Mega bonus for flag
        if 'lactf{' in text:
            s += 100000
            
        return s

with open('ct.txt') as f:
    ct = f.read()

clean = re.sub(r'[^a-zA-Z]', '', ct).lower()
clean += 'x' * ((3 - len(clean) % 3) % 3)
trigs = [clean[i:i+3] for i in range(0, len(clean), 3)]

p1, p2, p3 = [t[0] for t in trigs], [t[1] for t in trigs], [t[2] for t in trigs]

freq_en = 'etaoinshrdlcumwfgypbvkjxqz'
c1, c2, c3 = Counter(p1), Counter(p2), Counter(p3)

ct1 = [c for c, _ in c1.most_common()]
ct2 = [c for c, _ in c2.most_common()]
ct3 = [c for c, _ in c3.most_common()]

m1 = {ct1[i]: freq_en[i] for i in range(len(ct1))}
m2 = {ct2[i]: freq_en[i] for i in range(len(ct2))}
m3 = {ct3[i]: freq_en[i] for i in range(len(ct3))}

# Constraint from known njl -> lac
m1['n'] = 'l'
m2['j'] = 'a'
m3['l'] = 'c'

scorer = NGramScore()

def dec(m1, m2, m3):
    return ''.join([m1[t[0]] + m2[t[1]] + m3[t[2]] for t in trigs])

best = (m1.copy(), m2.copy(), m3.copy())
bs = scorer.score(dec(*best))
curr = best
cs = bs
temp = 1000.0
cool = 0.99998

print(f"Initial: {bs:.2f}")

for it in range(2000000):
    pos = random.choice([0, 1, 2])
    new = list(curr)
    
    fixed = ['n', 'j', 'l'][pos]
    keys = [k for k in new[pos].keys() if k != fixed]
    if len(keys) < 2:
        continue
    
    k1, k2 = random.sample(keys, 2)
    new[pos] = new[pos].copy()
    new[pos][k1], new[pos][k2] = new[pos][k2], new[pos][k1]
    
    ns = scorer.score(dec(*new))
    delta = ns - cs
    
    if delta > 0 or (temp > 0.5 and random.random() < math.exp(delta / temp)):
        curr = tuple(new)
        cs = ns
        
        if cs > bs:
            best = curr
            bs = cs
            if it % 100000 == 0:
                print(f"{it}: {bs:.2f}")
    
    temp *= cool
    
    if bs > 50000:
        print(f"Solution found at {it}!")
        break

result = dec(*best)
print("="*80)
print(result)

if 'lactf{' in result:
    i = result.find('lactf{')
    j = result.find('}', i)
    if j > 0:
        # Reconstruct with braces
        print("="*80)
        print(f"FLAG: {result[i:j+1]}")
    else:
        print("="*80)
        print(f"FLAG starts at {i}: {result[i:i+80]}")
