import re

# Read the ciphertext
with open('ct.txt', 'r') as f:
    ct = f.read()

# Clean the ciphertext
clean_ct = re.sub(r'[^a-zA-Z]', '', ct).lower()
if len(clean_ct) % 3 != 0:
    clean_ct += (3 - len(clean_ct) % 3) * 'x'

ct_trigrams = [clean_ct[i*3:(i+1)*3] for i in range(len(clean_ct)//3)]

# We know: njlel{...} -> lactf{...}
# So: njl -> lac, el{ -> tf{

# Let's find where this occurs
flag_start = None
for i in range(len(ct_trigrams)):
    if i < len(ct_trigrams) - 1:
        if ct_trigrams[i] == 'njl' and ct_trigrams[i+1] == 'el':
            flag_start = i
            print(f"Found 'njlel' at position {i}")
            break

# Extract the flag trigrams
if flag_start:
    # Find the closing brace
    flag_trigrams = []
    for i in range(flag_start, len(ct_trigrams)):
        trig = ct_trigrams[i]
        flag_trigrams.append(trig)
        # Check if this trigram ends with '}'
        test_str = ''.join(flag_trigrams)
        if '}' in ct[ct.find(test_str):ct.find(test_str)+len(test_str)+5]:
            break
    
    print(f"Flag trigrams: {flag_trigrams[:20]}")
    
# Known mappings from the visible flag structure
# njl -> lac
# Also the flag content is visible: njlel{heqmz_dgk_tevr_tk_vnnds_c_imcqaeyde_ug_byndu_e_jjaogy_rqqnisoqe_cwtnamd}

# Since we can see the actual ciphertext flag, let's map it
cipher_flag = "njlel{heqmz_dgk_tevr_tk_vnnds_c_imcqaeyde_ug_byndu_e_jjaogy_rqqnisoqe_cwtnamd}"

# Remove non-letters for trigram analysis
clean_cipher_flag = re.sub(r'[^a-z]', '', cipher_flag)
print(f"\nClean cipher flag: {clean_cipher_flag}")

# Split into trigrams
cipher_flag_trigrams = [clean_cipher_flag[i*3:(i+1)*3] for i in range(len(clean_cipher_flag)//3)]
print(f"Cipher flag trigrams: {cipher_flag_trigrams}")

# We know njl -> lac
# So we need to figure out the pattern
# The cipher creates: [chr(i)+chr(j)+chr(k) for i in shufflei for j in shufflej for k in shufflek]

# Let's try to brute force or use frequency analysis on the whole text
# with the constraint that njl -> lac

print("\n" + "="*80)
print("Let's use the fact that this is likely English text...")
print("="*80 + "\n")

# Create a smarter solver
# Since trigrams are independent substitutions, we can try an iterative approach

# Start with some known words/patterns
mapping = {
    'njl': 'lac',  # From flag
}

# Try common English trigrams for the most frequent ciphertext trigrams
from collections import Counter
trigram_freq = Counter(ct_trigrams)

print("Most frequent trigrams:")
for trig, count in trigram_freq.most_common(10):
    print(f"{trig}: {count}")
