import re
from collections import Counter

# Read the ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

# Clean the ciphertext
clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += (3 - len(clean_ct) % 3) * 'x'

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# Start with a simple frequency-based mapping
trigram_freq = Counter(ct_trigrams)
most_common_ct = [t for t, _ in trigram_freq.most_common()]

# Common English trigrams in order
common_english = ['the', 'and', 'ing', 'ion', 'tio', 'ent', 'ati', 'for', 'her', 'ter', 
                  'hat', 'tha', 'ere', 'ate', 'his', 'con', 'res', 'ver', 'all', 'ons',
                  'nce', 'est', 'ons', 'int', 'ite', 'red', 'ral', 'not', 'was', 'ect']

# Create initial mapping
mapping = {}
for i, ct_trig in enumerate(most_common_ct[:len(common_english)]):
    mapping[ct_trig] = common_english[i]

# Try decryption
def decrypt(ct_trigrams, mapping):
    result = []
    for trig in ct_trigrams:
        if trig in mapping:
            result.append(mapping[trig])
        else:
            result.append(f"[{trig}]")
    return ''.join(result)

decrypted = decrypt(ct_trigrams, mapping)
print("Initial decryption attempt:")
print(decrypted[:500])
print("\n" + "="*80 + "\n")

# Look for the flag pattern - lactf{...}
# In trigrams: "lac" "tf{" "..." "}"
# But let's search for patterns

# Search for potential flag location
for i in range(len(ct_trigrams) - 5):
    chunk = ct_trigrams[i:i+6]
    test_map = mapping.copy()
    # Try mapping first trigram to "lac"
    test_map[chunk[0]] = "lac"
    test_map[chunk[1]] = "tf{"
    
    partial = decrypt(ct_trigrams[i:i+20], test_map)
    if "lactf{" in partial:
        print(f"Possible flag at position {i}:")
        print(partial)
        print()
