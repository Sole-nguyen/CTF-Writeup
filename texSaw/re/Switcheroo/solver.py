#!/usr/bin/env python3
"""
Solver for Switcheroo RE challenge

Analysis of the binary:
1. Input must be 27 characters long
2. The binary applies transformations and checks
3. Multiple switch operations are performed
"""

def switch_function(input_str, param):
    """
    Reverse engineered from function at 0x4012df
    This function modifies the string based on whether param is even or odd
    """
    result = list(input_str)
    length = len(result)
    
    if param % 2 == 0:  # Even case (0x4012fc)
        # First loop: for i in range(param)
        for i in range(param):
            # Calculate position: (i * param) % 27
            pos = (i * param) % 27
            # Add param to the character at that position
            result[pos] = chr(ord(result[pos]) + param)
        
        # Then call function at 0x4011b6 which does a different shuffle
        result = shuffle_function(result, param)
    else:  # Odd case (0x40137c)
        # First call shuffle function
        result = shuffle_function(result, param)
        
        # Then subtract: for i in range(param)
        for i in range(param):
            pos = (i + param) % 27
            result[pos] = chr(ord(result[pos]) - param)
    
    return ''.join(result)

def shuffle_function(input_list, param):
    """
    Reverse engineered from function at 0x4011b6
    This shuffles characters based on modulo 27
    """
    result = input_list[:]
    temp = result[:27]  # Make a copy
    
    # For i in range(27): result[((i + param) % 27)] = temp[i]
    for i in range(27):
        new_pos = (i + param) % 27
        result[new_pos] = temp[i]
    
    return result

# The checking function at 0x401729 has these checks:
# After calling switch with 5, 6, 0xd (13), 3, 0x18 (24), 0xa (10), 7:
# - result[0] must be 0x9b (155)
# - result[0xb] (11) must be 0x6f ('o') after switch(5) and switch(6)
# - result[0xe] (14) must be 0x52 ('R')
# - result[0x1a] (26) must be in range 0x73-0x77 ('s' to 'w')
# - result[8] must be 0x59 ('Y')
# - result[0xb] (11) must be 0x59 ('Y') [wait this changed from 'o'?]
# - result[0xc] (12) must be in range 0x74-0x77 ('t' to 'w')
# - result[0x14] (20) must be 0xb5 (181)
# - result[0xd] (13) must be 0x73 ('s')

# Let me trace through more carefully...

def check_constraints(s):
    """Check if the string meets all the constraints after transformations"""
    print(f"Checking: {repr(s)}")
    print(f"Checking: {[hex(ord(c)) for c in s]}")
    
    # Apply transformations in order
    s = switch_function(s, 5)
    print(f"After switch(5): {[hex(ord(c)) for c in s]}")
    
    s = switch_function(s, 6)
    print(f"After switch(6): {[hex(ord(c)) for c in s]}")
    
    # Check s[11] == 'o'
    if s[11] != 'o':
        print(f"FAIL: s[11] = {repr(s[11])} != 'o'")
        return False
    print(f"PASS: s[11] = 'o'")
    
    s = switch_function(s, 13)
    print(f"After switch(13): {[hex(ord(c)) for c in s]}")
    
    # Check s[14] == 'R'
    if s[14] != 'R':
        print(f"FAIL: s[14] = {repr(s[14])} != 'R'")
        return False
    print(f"PASS: s[14] = 'R'")
    
    s = switch_function(s, 3)
    print(f"After switch(3): {[hex(ord(c)) for c in s]}")
    
    s = switch_function(s, 24)
    print(f"After switch(24): {[hex(ord(c)) for c in s]}")
    
    # Check s[0] == 0x9b
    if ord(s[0]) != 0x9b:
        print(f"FAIL: s[0] = {hex(ord(s[0]))} != 0x9b")
        return False
    print(f"PASS: s[0] = 0x9b")
    
    # Check s[26] in range 0x73-0x77
    if not (0x73 <= ord(s[26]) <= 0x77):
        print(f"FAIL: s[26] = {hex(ord(s[26]))} not in range 0x73-0x77")
        return False
    print(f"PASS: s[26] in range")
    
    s = switch_function(s, 10)
    print(f"After switch(10): {[hex(ord(c)) for c in s]}")
    
    # Check s[8] == 'Y'
    if s[8] != 'Y':
        print(f"FAIL: s[8] = {repr(s[8])} != 'Y'")
        return False
    print(f"PASS: s[8] = 'Y'")
    
    # Check s[11] == 'Y' (note: this is different from the earlier check!)
    if s[11] != 'Y':
        print(f"FAIL: s[11] = {repr(s[11])} != 'Y'")
        return False
    print(f"PASS: s[11] = 'Y'")
    
    # Check s[12] in range 0x74-0x77
    if not (0x74 <= ord(s[12]) <= 0x77):
        print(f"FAIL: s[12] = {hex(ord(s[12]))} not in range 0x74-0x77")
        return False
    print(f"PASS: s[12] in range")
    
    s = switch_function(s, 7)
    print(f"After switch(7): {[hex(ord(c)) for c in s]}")
    
    # Check s[20] == 0xb5
    if ord(s[20]) != 0xb5:
        print(f"FAIL: s[20] = {hex(ord(s[20]))} != 0xb5")
        return False
    print(f"PASS: s[20] = 0xb5")
    
    # Check s[13] == 's'
    if s[13] != 's':
        print(f"FAIL: s[13] = {repr(s[13])} != 's'")
        return False
    print(f"PASS: s[13] = 's'")
    
    return True

# Test with a sample input
test_input = "a" * 27
if check_constraints(test_input):
    print(f"\nSUCCESS! The flag is: texsaw{{{test_input}}}")
else:
    print("\nFailed constraints")
