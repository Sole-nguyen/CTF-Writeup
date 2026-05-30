# Deadwater

## Challenge Description
A reverse engineering challenge involving a complex hashing/validation routine.

## Analysis
The `deadwater` binary expects a single 80-character hex string as input. 

### Technical Details:
- **Input:** 80-character hex string (representing 40 bytes)
- **Protection:** TSX-protected hashing routine
- **Algorithm:** Custom PRNG-based table generation and mixing

The program:
1. Parses the hex input into 40 bytes
2. Builds a 48×256 lookup table using a custom PRNG
3. Mixes each input byte with table-derived bytes
4. Checks against five 64-bit constants
5. Prints `yarrr` on success, `narrrr` or other decoys on failure

## Solution Approach

To solve this challenge offline:

1. **Reverse engineer the binary:**
   - Analyze the PRNG implementation
   - Understand the table generation algorithm
   - Identify the 64-bit validation constants

2. **Implement the PRNG:**
   - Replicate the exact PRNG logic from the disassembly
   - Generate the same 48×256 lookup tables

3. **Invert the mixing:**
   - Work backwards from the target constants
   - XOR with the appropriate table entries
   - Compute the required input preimage

4. **Submit the hex string:**
   - The computed 40-byte value in hex format
   - Submit to the binary to verify (should print "yarrr")

## Solution

The solve script (`solve.py`) implements:
- The custom PRNG with exact parameters from the binary
- 48-layer table generation with rotate-right operations
- State updates matching the disassembly
- Preimage computation by XORing target values with table entries

### Flag/Answer

The correct hex input that produces "yarrr":

```
52f8c23363f6e22fe711e30879413706db0c2cf209de2044d16f79e13f01c0518f3414a0642d4823
```

This 80-character hex string represents the 40 bytes that satisfy all validation checks.

**Note:** The hex string itself IS the solution. The flag format is: `RITSEC{52f8c23363f6e22fe711e30879413706db0c2cf209de2044d16f79e13f01c0518f3414a0642d4823}`
