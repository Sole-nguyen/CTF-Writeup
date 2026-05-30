#!/usr/bin/env python3
"""
Solver for Pierre's Compass - RITSEC CTF
Involves three Linear Congruential Generators (LCGs)

Challenge: Pierre's enchanted compass uses three LCGs working together.
We have the moduli and seeds, but need to find the multipliers (a) and increments (c).
"""

# Given parameters from params.txt
characters = "G!{Qq)EPU-M7yNAKnF%fS=\\Z?;+.T2/8Lx65'@*VBw,#k:|~Dr`eOa9H\"hb>3^<Jp}[&$iXogzl4vWu(tsc]1YmC_RI0jd"
m1, m2, m3 = 95, 37, 19
s1, s2, s3 = 11, 29, 7

# LCG formula: X_{n+1} = (a * X_n + c) mod m
# Solution found through brute force: a1=1, c1=1, a2=3, c2=9, a3=10, c3=7

def lcg(state, a, c, m):
    """Linear Congruential Generator"""
    return (a * state + c) % m

def decode_message(a1, c1, a2, c2, a3, c3, length=500):
    """Decode Pierre's message with given LCG parameters"""
    state1, state2, state3 = s1, s2, s3
    message = []
    
    for i in range(length):
        # Generate next states
        state1 = lcg(state1, a1, c1, m1)
        state2 = lcg(state2, a2, c2, m2)
        state3 = lcg(state3, a3, c3, m3)
        
        # Combine the three outputs by summing and taking modulo of alphabet length
        index = (state1 + state2 + state3) % len(characters)
        message.append(characters[index])
    
    return ''.join(message)

# Use the discovered parameters
a1, c1 = 1, 1
a2, c2 = 3, 9
a3, c3 = 10, 7

print("=" * 80)
print("Pierre's Compass Solver - RITSEC CTF")
print("=" * 80)
print(f"\nLCG Parameters:")
print(f"  Generator 1: a={a1}, c={c1}, m={m1}, seed={s1}")
print(f"  Generator 2: a={a2}, c={c2}, m={m2}, seed={s2}")
print(f"  Generator 3: a={a3}, c={c3}, m={m3}, seed={s3}")
print(f"\nAlphabet length: {len(characters)}")

# Decode the message (need 500+ chars to get the full flag)
full_message = decode_message(a1, c1, a2, c2, a3, c3, 500)

# Extract the flag
if "RS{" in full_message:
    flag_start = full_message.index("RS{")
    # Search for closing brace after RS{
    # The flag is quite long (238 characters!)
    flag_end = -1
    for i in range(flag_start + 3, len(full_message)):
        if full_message[i] == "}":
            flag_end = i + 1
            break
    
    if flag_end > 0:
        flag = full_message[flag_start:flag_end]
        
        print(f"\n{'=' * 80}")
        print("FLAG FOUND!")
        print(f"{'=' * 80}")
        print(f"\n{flag}\n")
        print(f"{'=' * 80}")
        print(f"Flag length: {len(flag)} characters")
    else:
        print("\nWarning: Could not find closing brace for flag")
        print(f"Message starting from RS{{: {full_message[flag_start:flag_start+50]}")
else:
    print("\nWarning: Flag format RS{} not found in decoded message")
    print("Full output shown above for manual inspection")
