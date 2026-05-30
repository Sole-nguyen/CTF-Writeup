#!/usr/bin/env python3
"""
Trigram substitution cipher solver using frequency analysis and known plaintext.
We know the flag starts with "lactf{" which gives us some known mappings.
"""
import re
from collections import Counter, defaultdict

# Read the ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

# Clean the ciphertext
clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += (3 - len(clean_ct) % 3) * 'x'

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

print(f"Total trigrams: {len(ct_trigrams)}")
print(f"Unique trigrams: {len(set(ct_trigrams))}")

# Find common patterns
freq = Counter(ct_trigrams)
print("\nTop 30 most common trigrams:")
for trig, count in freq.most_common(30):
    print(f"  {trig}: {count}")

# We know from the ciphertext that the flag appears to be:
# njlel{heqmz_dgk_tevr_tk_vnnds_c_imcqaeyde_ug_byndu_e_jjaogy_rqqnisoqe_cwtnamd}

# Since flag format is lactf{...}, we have:
# njl -> lac
# el? -> tf? (but there's a { after el in the ciphertext)

# Let me check where the flag is in the trigram sequence
flag_cipher = "njlelheqmzdgktevrtkvnndscimcqaeydeugbynduejjaogyrqqnisoqecwtnamd"
flag_trigrams_cipher = [flag_cipher[i*3:(i+1)*3] for i in range(len(flag_cipher)//3)]
print(f"\nFlag cipher trigrams: {flag_trigrams_cipher}")

# The plaintext should be: lactf{...}
# Let's assume the flag plaintext is something like: lactf{some_text_here}

# From flag format, we can deduce:
# Position 0: njl -> lac
# Position 1: elh -> tf{ (but tf{ is only 3 chars, with { being special)

# Actually, looking at the encryption function, special characters are preserved!
# So the trigrams only cover letters.

# Let's look at common English trigrams
common_english = [
    'the', 'and', 'ing', 'ent', 'ion', 'her', 'for', 'tha', 'nth', 'int',
    'ere', 'tio', 'ter', 'est', 'ers', 'ati', 'hat', 'ate', 'his', 'res',
    'rea', 'sth', 'eth', 'han', 'sta', 'ene', 'hes', 'ear', 'eve', 'ona'
]

# Assuming most frequent cipher trigrams map to most frequent English trigrams
mapping = {}
most_common_ct = [t for t, c in freq.most_common(30)]

for i, ct_trig in enumerate(most_common_ct):
    if i < len(common_english):
        mapping[ct_trig] = common_english[i]

# Override with known: njl -> lac
mapping['njl'] = 'lac'

# Try decryption
def decrypt(ct_trigs, mapping):
    result = []
    for trig in ct_trigs:
        if trig in mapping:
            result.append(mapping[trig])
        else:
            result.append(f"?{trig}?")
    return ''.join(result)

decrypted = decrypt(ct_trigrams, mapping)
print("\n" + "="*80)
print("Decrypted text (partial):")
print("="*80)
print(decrypted[:500])

# Find flag in output
print("\n" + "="*80)
print("Flag area:")
print("="*80)
flag_start_idx = None
for i, trig in enumerate(ct_trigrams):
    if trig == 'njl':
        flag_start_idx = i
        break

if flag_start_idx:
    flag_area = decrypt(ct_trigrams[flag_start_idx:flag_start_idx+30], mapping)
    print(flag_area)
