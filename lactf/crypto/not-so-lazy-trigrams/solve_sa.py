#!/usr/bin/env python3
"""
Better trigram solver using simulated annealing with English text scoring.
"""
import re
import random
import math
from collections import Counter

# English letter frequencies
ENGLISH_FREQ = {
    'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
    's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
    'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
    'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

# Common English trigrams
COMMON_TRIGRAMS = set([
    'the', 'and', 'ing', 'ent', 'ion', 'her', 'for', 'tha', 'nth', 'int',
    'ere', 'tio', 'ter', 'est', 'ers', 'ati', 'hat', 'ate', 'all', 'eth',
    'hes', 'ver', 'his', 'oft', 'ith', 'fth', 'sth', 'oth', 'res', 'ont',
])

# Common English bigrams  
COMMON_BIGRAMS = set(['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of', 'ed', 'is', 'it', 'al', 'ar', 'st', 'to', 'nt', 'ng', 'se', 'ha', 'as', 'ou', 'io', 'le'])

# Common English words
COMMON_WORDS = set(['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'time', 'very', 'when', 'your', 'come', 'from', 'have', 'just', 'like', 'long', 'make', 'many', 'over', 'some', 'than', 'that', 'them', 'then', 'this', 'with', 'would'])

# Read ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += 'x' * (3 - len(clean_ct) % 3)

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]
unique_ct = list(set(ct_trigrams))

# Generate all possible plaintext trigrams
all_pt_trigrams = [chr(i)+chr(j)+chr(k) for i in range(97,123) for j in range(97,123) for k in range(97,123)]

def decrypt(ct_trigs, mapping):
    return ''.join([mapping.get(t, '   ') for t in ct_trigs])

def score_text(text):
    """Score decrypted text based on English language patterns."""
    score = 0.0
    
    # Score based on common trigrams
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in COMMON_TRIGRAMS:
            score += 3
    
    # Score based on common bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in COMMON_BIGRAMS:
            score += 1
    
    # Score based on common words
    words = text.split()
    for word in words:
        if word in COMMON_WORDS:
            score += 5
    
    # Score based on letter frequency
    letter_counts = Counter(text.replace(' ', ''))
    total = sum(letter_counts.values())
    if total > 0:
        for letter, expected_freq in ENGLISH_FREQ.items():
            actual_freq = (letter_counts.get(letter, 0) / total) * 100
            score -= abs(actual_freq - expected_freq) * 0.1
    
    # Penalize rare letter combinations
    rare_bigrams = ['qz', 'jz', 'qx', 'jx', 'wx', 'vx', 'zx']
    for rb in rare_bigrams:
        score -= text.count(rb) * 5
    
    return score

# Simulated annealing
def simulated_annealing(ct_trigs, unique_ct, temp=100, cooling=0.99, iterations=50000):
    # Initial random mapping
    current_mapping = dict(zip(unique_ct, random.sample(all_pt_trigrams, len(unique_ct))))
    current_score = score_text(decrypt(ct_trigs, current_mapping))
    
    best_mapping = current_mapping.copy()
    best_score = current_score
    
    for i in range(iterations):
        # Make a small change
        new_mapping = current_mapping.copy()
        
        # Swap two random mappings
        k1, k2 = random.sample(unique_ct, 2)
        new_mapping[k1], new_mapping[k2] = new_mapping[k2], new_mapping[k1]
        
        new_score = score_text(decrypt(ct_trigs, new_mapping))
        
        # Accept if better, or with probability based on temperature
        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(delta / temp):
            current_mapping = new_mapping
            current_score = new_score
            
            if current_score > best_score:
                best_mapping = current_mapping.copy()
                best_score = current_score
        
        # Cool down
        temp *= cooling
        
        if i % 5000 == 0:
            print(f"Iteration {i}: best_score = {best_score:.2f}, temp = {temp:.2f}")
    
    return best_mapping, best_score

print("Starting simulated annealing...")
print(f"Unique ciphertext trigrams: {len(unique_ct)}")

best_mapping, best_score = simulated_annealing(ct_trigrams, unique_ct)

print("\n" + "="*80)
print(f"Best score: {best_score:.2f}")
print("="*80)

decrypted = decrypt(ct_trigrams, best_mapping)
print(decrypted)

# Look for flag
print("\n" + "="*80)
print("Looking for flag pattern...")
print("="*80)
if 'lactf{' in decrypted:
    flag_start = decrypted.find('lactf{')
    flag_end = decrypted.find('}', flag_start)
    if flag_end > 0:
        flag = decrypted[flag_start:flag_end+1]
        print(f"\nFOUND FLAG: {flag}")
