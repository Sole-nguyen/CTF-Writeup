# -*- coding: utf-8 -*-
"""
Template for decoding once you know the per-byte transformations from IDA
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

# TODO: Fill in the decode_byte_X functions based on IDA analysis
# Each function should reverse the transformation for that byte position

def decode_byte_0(enc):
    # From IDA: determine what operation was used
    # Example: if it was XOR 0x10, then:
    return enc ^ 0x10

# def decode_byte_1(enc):
#     # Fill in based on IDA
#     pass

# ... etc for all 42 bytes

# Once you have all transformations:
# result = []
# decode_funcs = [decode_byte_0, decode_byte_1, ...]  # All 42 functions
# for i in range(42):
#     result.append(decode_funcs[i](data[i]))
#
# flag = bytes(result).decode('ascii')
# print(flag)

print("Please analyze the binary in IDA and fill in the decode functions above.")
print("\nLook for:")
print("- Functions named f_10 through f_74")
print("- The main function's comparison logic")
print("- How each byte of input is transformed before comparison")
