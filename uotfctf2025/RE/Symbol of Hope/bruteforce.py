# -*- coding: utf-8 -*-
import itertools

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

def check_printable(result):
    """Check if result is mostly printable ASCII"""
    try:
        text = bytes(result).decode('ascii')
        if text.startswith('uoftctf{') and text.endswith('}'):
            return True, text
    except:
        pass
    return False, None

# Maybe it's a combination of multiple operations
operations = {
    'ror1': lambda b: ror(b, 1),
    'ror2': lambda b: ror(b, 2),
    'ror3': lambda b: ror(b, 3),
    'ror4': lambda b: ror(b, 4),
    'rol1': lambda b: rol(b, 1),
    'rol2': lambda b: rol(b, 2),
    'rol3': lambda b: rol(b, 3),
    'rol4': lambda b: rol(b, 4),
    'xor0x10': lambda b: b ^ 0x10,
    'xor0x20': lambda b: b ^ 0x20,
    'xor0x55': lambda b: b ^ 0x55,
    'xorAA': lambda b: b ^ 0xAA,
    'add1': lambda b: (b + 1) & 0xFF,
    'sub1': lambda b: (b - 1) & 0xFF,
    'not': lambda b: (~b) & 0xFF,
}

print("Trying single operations...")
for op_name, op_func in operations.items():
    result = [op_func(b) for b in data]
    is_flag, text = check_printable(result)
    if is_flag:
        print(f"\n*** FOUND FLAG with {op_name} ***")
        print(text)
        exit()

print("\nTrying combinations of 2 operations...")
for op1_name in operations:
    for op2_name in operations:
        result = [operations[op2_name](operations[op1_name](b)) for b in data]
        is_flag, text = check_printable(result)
        if is_flag:
            print(f"\n*** FOUND FLAG with {op1_name} -> {op2_name} ***")
            print(text)
            exit()

print("\nTrying reverse byte order...")
result = data[::-1]
is_flag, text = check_printable(result)
if is_flag:
    print(f"\n*** FOUND FLAG with reverse ***")
    print(text)

print("\nTrying nibble swap...")
result = [((b & 0x0F) << 4) | ((b & 0xF0) >> 4) for b in data]
is_flag, text = check_printable(result)
if is_flag:
    print(f"\n*** FOUND FLAG with nibble swap ***")
    print(text)

print("\nTrying bit reversal...")
def reverse_bits(b):
    result = 0
    for i in range(8):
        result = (result << 1) | ((b >> i) & 1)
    return result

result = [reverse_bits(b) for b in data]
is_flag, text = check_printable(result)
if is_flag:
    print(f"\n*** FOUND FLAG with bit reversal ***")
    print(text)

# Print the results anyway to see patterns
print(f"\nNibble swap result: {bytes([(b & 0x0F) << 4 | (b & 0xF0) >> 4 for b in data])}")
print(f"Bit reversal result: {bytes([reverse_bits(b) for b in data])}")
print(f"NOT result: {bytes([(~b) & 0xFF for b in data])}")
