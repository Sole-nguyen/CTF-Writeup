import re
from collections import Counter

with open('ct.txt') as f:
    ct = f.read()

clean = re.sub(r'[^a-zA-Z]', '', ct).lower()
clean += 'x' * ((3 - len(clean) % 3) % 3)
trigs = [clean[i:i+3] for i in range(0, len(clean), 3)]

# From known and guesses:
# njl -> lac: n->l, j->a, l->c
# jqu -> the: j->t, q->h, u->e  
# zjn -> and: z->a, j->n, n->d

# But wait, conflicts:
# Position 0: j can't be both 't' (from jqu) and stay as 'j'
# Position 1: j->a (from njl) vs j->n (from zjn) CONFLICT!
# Position 2: n->d (from zjn) vs l->c (from njl)

# I made a mistake - let me reconsider
# Position 0 (first char of trigram): n->l from njl
# Position 1 (second char): j->a from njl  
# Position 2 (third char): l->c from njl

# For jqu (if it's 'the'):
# Position 0: j->t
# Position 1: q->h
# Position 2: u->e

# For zjn (if it's 'and'):
# Position 0: z->a
# Position 1: j->n (CONFLICTS with j->a from njl!)
# Position 2: n->d

# So zjn can't be 'and' because j is already mapped to 'a' in position 1

# Let me be more careful. Let me try kte -> ing (3rd most common)
# Position 0: k->i
# Position 1: t->n
# Position 2: e->g

m1 = {'n': 'l', 'j': 't', 'k': 'i'}
m2 = {'j': 'a', 'q': 'h', 't': 'n'}
m3 = {'l': 'c', 'u': 'e', 'e': 'g'}

def decrypt(trigs, m1, m2, m3):
    result = []
    for t in trigs:
        result.append(m1.get(t[0], '?') + m2.get(t[1], '?') + m3.get(t[2], '?'))
    return ''.join(result)

dec = decrypt(trigs, m1, m2, m3)
print("With jqu->the, kte->ing:")
print(dec[:300])
print()

# Let's look at what trigrams we can now partially see
print("Looking for patterns...")
words = dec.split('???')
for w in words[:20]:
    if len(w) > 3 and '?' not in w[:4]:
        print(f"  {w[:15]}")

# Let's find more common trigrams and guess
freq = Counter(trigs)
print("\nMost common trigrams:")
for trig, count in freq.most_common(15):
    partial = m1.get(trig[0], '?') + m2.get(trig[1], '?') + m3.get(trig[2], '?')
    print(f"  {trig} ({count}): {partial}")
