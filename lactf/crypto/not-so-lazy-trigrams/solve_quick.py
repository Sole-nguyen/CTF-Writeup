#!/usr/bin/env python3
"""
Use quadgram/trigram statistics from a corpus for better scoring.
This is a simplified version that runs faster.
"""
import re
import random
import math
from collections import Counter, defaultdict

# Read ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += 'x' * (3 - len(clean_ct) % 3)

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# Try using a different approach: use the known flag structure
# We know njl -> lac from the flag

# Let me try to use a corpus or known text to build better frequency data
# For now, let's use IOC (Index of Coincidence) and common patterns

def decrypt(ct_trigs, mapping):
    result = []
    for t in ct_trigs:
        result.append(mapping.get(t, '___'))
    return ''.join(result)

# Use word pattern matching
# Let's assume the text contains common English phrases

def quick_solve():
    # Start with the most frequent trigrams mapping to common English
    freq = Counter(ct_trigrams)
    most_common_ct = [t for t, c in freq.most_common()]
    
    common_english = [
        'the', 'and', 'ing', 'tion', 'for', 'her', 'hat', 'ter', 'his', 'tha',
        'ere', 'ate', 'ent', 'ion', 'est', 'ers', 'tio', 'all', 'that', 'with',
        'res', 'ver', 'was', 'not', 'are', 'but', 'can', 'you', 'one', 'out'
    ]
    
    # Try multiple random starts
    best_result = None
    best_score = -999999
    
    for attempt in range(50):
        mapping = {}
        
        # Keep njl -> lac fixed (we know this from flag)
        mapping['njl'] = 'lac'
        
        # Randomly assign others but bias towards frequency
        remaining_ct = [t for t in most_common_ct if t != 'njl']
        remaining_pt = [t for t in common_english if t != 'lac']
        
        # Add more random trigrams
        all_pt = [chr(i)+chr(j)+chr(k) for i in range(97,123) for j in range(97,123) for k in range(97,123)]
        remaining_pt += random.sample([t for t in all_pt if t not in remaining_pt], 
                                     min(len(remaining_ct) - len(remaining_pt), len(all_pt) - len(remaining_pt)))
        
        random.shuffle(remaining_pt)
        for i, ct in enumerate(remaining_ct):
            if i < len(remaining_pt):
                mapping[ct] = remaining_pt[i]
        
        # Decrypt
        decrypted = decrypt(ct_trigrams, mapping)
        
        # Simple scoring
        score = 0
        score += decrypted.count(' the ') * 10
        score += decrypted.count(' and ') * 8
        score += decrypted.count('ing ') * 5
        score += decrypted.count('tion') * 5
        score += decrypted.count('lactf{') * 1000  # Heavily weight finding the flag!
        
        if score > best_score:
            best_score = score
            best_result = (decrypted, mapping)
        
        if attempt % 10 == 0:
            print(f"Attempt {attempt}: score = {best_score}")
    
    return best_result

print("Running quick solve with random trials...")
decrypted, mapping = quick_solve()

print("\n" + "="*80)
print("Best decryption found:")
print("="*80)
print(decrypted)

# Extract flag
if 'lactf{' in decrypted:
    flag_start = decrypted.find('lactf{')
    flag_end = decrypted.find('}', flag_start)
    if flag_end > 0:
        flag = decrypted[flag_start:flag_end+1]
        print("\n" + "="*80)
        print(f"FLAG FOUND: {flag}")
        print("="*80)
else:
    print("\nFlag not found yet, trying to locate it manually...")
    # Find njl
    for i, trig in enumerate(ct_trigrams):
        if trig == 'njl':
            print(f"\nFound 'njl' at position {i}:")
            context = decrypt(ct_trigrams[max(0,i-5):i+20], mapping)
            print(f"  {context}")
