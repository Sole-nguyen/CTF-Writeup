#!/usr/bin/env python3

def solve_lcg():
    # The sequence you provided
    targets = [33, 13, 89, 42, 11, 35, 98, 98, 37, 86]

    # LCG Parameters from your challenge code
    M = 2147483647
    A = 48271
    C = 12345

    print(f"[*] Cracking LCG state based on sequence: {targets}")
    print("[*] Brute-forcing ~21 million possible states. Please wait...")

    # We know the first output is 46, so the first state must be (k * 100) + 46
    # We iterate k to find the matching state.
    for k in range(M // 100 + 1):
        # Reconstruct potential state S1
        s1 = k * 100 + targets[0]
        
        # Optimization check: 
        # Calculate S2 and check if it matches the second target (72)
        # This filters out 99% of wrong candidates instantly.
        s2 = (A * s1 + C) % M
        if s2 % 100 == targets[1]:
            
            # If S2 matches, check the rest of the sequence (S3, S4...)
            current_state = s2
            match = True
            for i in range(2, len(targets)):
                current_state = (A * current_state + C) % M
                if current_state % 100 != targets[i]:
                    match = False
                    break
            
            if match:
                print(f"[+] FOUND STATE S1: {s1}")
                print(f"[+] Verifying sequence ends with: {targets[-1]}")
                
                # We are currently at the state corresponding to the last target (55)
                # Now generate the next 5 spins
                next_spins = []
                for _ in range(5):
                    current_state = (A * current_state + C) % M
                    next_spins.append(str(current_state % 100))
                
                print("\nPREDICTION FOUND:")
                print(" ".join(next_spins))
                return

solve_lcg()