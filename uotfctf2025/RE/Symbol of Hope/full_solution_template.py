# -*- coding: utf-8 -*-
"""
FULL SOLUTION TEMPLATE
Fill in ALL 42 functions from IDA analysis

Pattern observed:
- f_0: position 4, add 0x0A
- f_11: position 38, add 0x70  
- f_12: position 39, xor 0xA7

Continue this pattern for all functions!
"""

data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

def ror(val, n):
    return ((val >> n) | (val << (8 - n))) & 0xFF

def rol(val, n):
    return ((val << n) | (val >> (8 - n))) & 0xFF

# DECRYPT operations (inverse of encryption)
# Format: position: ('operation', value)
# Remember: 
#   - encrypt ADD → decrypt SUB
#   - encrypt SUB → decrypt ADD
#   - encrypt XOR → decrypt XOR (same)

decrypt_ops = {
    # TODO: Fill in by analyzing each function in IDA
    # Look for: add rax, XXh (position), then add/sub/xor edx, YYh (operation)
    
    # From f_0:
    4: ('sub', 0x0A),   # encrypt: add 0x0A
    
    # From f_1 to f_10: (need to analyze in IDA)
    # ...
    
    # From f_11:
    38: ('sub', 0x70),  # encrypt: add 0x70
    
    # From f_12:
    39: ('xor', 0xA7),  # encrypt: xor 0xA7
    
    # Continue for all remaining functions...
}

print("="*60)
print("INSTRUCTIONS TO COMPLETE:")
print("="*60)
print("1. In IDA, go to Functions window (Shift+F3)")
print("2. For EACH function from f_0 to f_74:")
print("   a. Double-click the function")
print("   b. Find 'add rax, XXh' -> this is the POSITION (in hex)")
print("   c. Find 'add/sub/xor edx, YYh' -> this is the OPERATION")
print("   d. Add to decrypt_ops dictionary above with INVERSE operation")
print()
print("Quick guide:")
print("  - If you see 'add edx, 0x50' -> write: pos: ('sub', 0x50)")
print("  - If you see 'sub edx, 0x30' -> write: pos: ('add', 0x30)")
print("  - If you see 'xor edx, 0x12' -> write: pos: ('xor', 0x12)")
print("="*60)

# Try to decrypt with current operations
result = list(data)
for pos, (op, val) in decrypt_ops.items():
    if op == 'add':
        result[pos] = (result[pos] + val) & 0xFF
    elif op == 'sub':
        result[pos] = (result[pos] - val) & 0xFF
    elif op == 'xor':
        result[pos] = result[pos] ^ val
    elif op == 'rol':
        result[pos] = rol(result[pos], val)
    elif op == 'ror':
        result[pos] = ror(result[pos], val)

print(f"\nPositions configured: {len(decrypt_ops)}/42")
print(f"Positions: {sorted(decrypt_ops.keys())}\n")

try:
    partial = bytes(result).decode('latin-1')
    print(f"Current partial decrypt: {repr(partial)}")
    
    # Show what we got for known positions
    if result[4] == ord('c'):  # position 4 should be 'c' from "uoftctf{"
        print("✓ Position 4 correct!")
    else:
        print(f"✗ Position 4: expected 'c', got '{chr(result[4]) if 32<=result[4]<127 else '?'}'")
        
except Exception as e:
    print(f"Decode error: {e}")

print("\n" + "="*60)
print("Once you fill in ALL 42 operations, run this script again!")
print("="*60)
