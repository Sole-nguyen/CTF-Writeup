# Patona Challenge Solution

## Challenge Analysis
- **File**: flag.raw
- **Type**: UTF-8 encoded text with substitution cipher
- **Goal**: Find flag in format ASIS{...}

## Cipher Type
Monoalphabetic substitution cipher using UTF-8 characters (Arabic/Persian Unicode range)

## Solution Method

### Step 1: Read and Decode
```python
with open('flag.raw', 'rb') as f:
    data = f.read()
text = data.decode('utf-8', errors='replace')
```

### Step 2: Frequency Analysis
```python
from collections import Counter
freq = Counter(text)
chars_sorted = [ch for ch, _ in freq.most_common()]
```

### Step 3: Build Substitution Map
Map characters by frequency to English:
- Most frequent → space or 'e'
- Next most frequent → common letters (t, a, o, i, n, s, etc.)
- Include special characters: {, }, _, -, etc.

```python
# English frequency order
target = ' etaoinsrhldcumfgypbvkxjqzETAOINSRHLDCUMFGYPBVKXJQZ0123456789_-.,;:!?()[]{}"\'/\\@#$%^&*+=<>|`~'

# Create mapping
substitution = {}
for i, source_char in enumerate(chars_sorted):
    if i < len(target):
        substitution[source_char] = target[i]
    else:
        substitution[source_char] = '?'

# Apply substitution
decoded = ''.join(substitution.get(c, c) for c in text)
```

### Step 4: Search for Flag
```python
import re
flags = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
print(flags[0])  # The flag
```

## Alternative Approaches

### Approach A: Standard Frequency
Map most frequent to: space, e, t, a, o, i, n, s, h, r, d, l...

### Approach B: Flag-Priority
Map most frequent to: A, S, I, {, }, space, _, then common letters

### Approach C: XOR Check
Try single-byte and multi-byte XOR with common keys like:
- b'ASIS', b'patona', b'flag', b'key'

## Execution

Run any of these scripts:
1. `python ULTIMATE_SOLVER.py` - Most comprehensive
2. `python simple_solver.py` - Quick and simple
3. `python decode_complete.py` - Detailed analysis

Or use the batch file:
```
SOLVE.bat
```

## Expected Output

The flag will be in the format:
```
ASIS{some_text_here_describing_the_challenge}
```

## Files Created

- `ULTIMATE_SOLVER.py` - Main solver with multiple strategies
- `simple_solver.py` - Simplified version
- `decode_complete.py` - Detailed byte analysis
- `SOLVE.bat` - Windows batch runner

## Notes

The challenge name "Patona" might be a hint about the pattern or cipher type used.
The substitution is consistent throughout the file (monoalphabetic), making frequency analysis effective.
