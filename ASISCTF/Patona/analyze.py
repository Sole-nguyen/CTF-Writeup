import sys

# Read raw bytes
with open('flag.raw', 'rb') as f:
    data = f.read()

# The file contains UTF-8 encoded Arabic/Persian characters
# Let me decode and analyze the text
text = data.decode('utf-8', errors='ignore')

print("Text length:", len(text))
print("First 200 chars:", repr(text[:200]))

# Count unique characters
unique_chars = set(text)
print(f"\nUnique characters: {len(unique_chars)}")
print("Unique chars:", ''.join(sorted(unique_chars)))

# The repeating pattern suggests substitution cipher
# Common repeating sequences
from collections import Counter

# Look for character frequencies
freq = Counter(text)
print("\nTop 20 most common characters:")
for char, count in freq.most_common(20):
    print(f"  '{char}' (U+{ord(char):04X}): {count} times")

# Try to identify the mapping
# ASIS{} flag format means we need:
# A S I S { }
# Let's look for patterns

# Find most common patterns
print("\n2-char patterns:")
bigrams = Counter([text[i:i+2] for i in range(len(text)-1)])
for bg, count in bigrams.most_common(10):
    print(f"  '{bg}': {count}")

print("\n3-char patterns:")
trigrams = Counter([text[i:i+3] for i in range(len(text)-2)])
for tg, count in trigrams.most_common(10):
    print(f"  '{tg}': {count}")
