#!/usr/bin/env python3
import re
from collections import Counter
import random

# Read the ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

# Clean the ciphertext
clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += (3 - len(clean_ct) % 3) * 'x'

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# Load English trigram frequencies (simplified)
# Most common English trigrams
english_trigrams = {
    'the': 1.81, 'and': 0.73, 'ing': 0.72, 'ion': 0.42, 'tio': 0.34,
    'ent': 0.42, 'ati': 0.36, 'for': 0.34, 'her': 0.33, 'ter': 0.31,
    'hat': 0.30, 'tha': 0.30, 'ere': 0.28, 'ate': 0.26, 'his': 0.24,
    'con': 0.22, 'res': 0.21, 'ver': 0.19, 'all': 0.19, 'ons': 0.18,
}

# Get all unique trigrams in ciphertext
unique_ct = list(set(ct_trigrams))
print(f"Total unique trigrams in ciphertext: {len(unique_ct)}")

# Generate all possible plaintext trigrams
all_pt_trigrams = [chr(i)+chr(j)+chr(k) for i in range(97,123) for j in range(97,123) for k in range(97,123)]
print(f"Total possible trigrams: {len(all_pt_trigrams)}")

# Scoring function based on English frequency
def score_text(text):
    score = 0.0
    # Check for common English words
    common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'have', 'this', 'that', 'with']
    for word in common_words:
        score += text.count(word) * 10
    
    # Check for common letter patterns
    score += text.count('tion') * 5
    score += text.count('ing ') * 5
    score += text.count(' the ') * 10
    score += text.count(' and ') * 8
    
    # Penalize unusual patterns
    score -= text.count('qq') * 5
    score -= text.count('zz') * 3
    score -= text.count('xxx') * 10
    
    return score

# Start with random mapping
def create_random_mapping(ct_trigrams_unique, all_pt):
    pt_sample = random.sample(all_pt, len(ct_trigrams_unique))
    return dict(zip(ct_trigrams_unique, pt_sample))

def decrypt_with_mapping(ct_trig_list, mapping):
    return ''.join([mapping.get(t, '???') for t in ct_trig_list])

# Hill climbing
print("\nStarting hill climbing...")
best_mapping = create_random_mapping(unique_ct, all_pt_trigrams)
best_score = score_text(decrypt_with_mapping(ct_trigrams, best_mapping))

iterations = 10000
for iter in range(iterations):
    # Make a small change
    new_mapping = best_mapping.copy()
    
    # Swap two random mappings
    keys = list(new_mapping.keys())
    k1, k2 = random.sample(keys, 2)
    new_mapping[k1], new_mapping[k2] = new_mapping[k2], new_mapping[k1]
    
    new_score = score_text(decrypt_with_mapping(ct_trigrams, new_mapping))
    
    if new_score > best_score:
        best_score = new_score
        best_mapping = new_mapping
        if iter % 100 == 0:
            print(f"Iteration {iter}: score = {best_score}")
            decrypted = decrypt_with_mapping(ct_trigrams, best_mapping)
            print(f"Sample: {decrypted[:100]}")

print("\n" + "="*80)
print("Best decryption:")
decrypted = decrypt_with_mapping(ct_trigrams, best_mapping)
print(decrypted)
