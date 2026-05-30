#!/usr/bin/env python3
"""
Last resort: Use RsaCtfTool or try online factorization services
"""

import subprocess
import sys

n = 24436555811992972366076806922530312273907496823566498825278523886197470905017391954938641972382127780163747562797956038193398654235644409459287830339446234525262072627164429789264587184451084484976035579016063031028571643546268940916664832350416704133070528632744931737357768415126788528052461206333395794164406084571633391115829776964808677724703621221154710591190375698378697896449037181113710774632252351521950724961537615755537875194862156989318761303971336544564950137455452434307027177388197740176937447577518701185717201408469263753367188476145954061480542913006467287367140336404472235624010067372903582272729
n_hex = hex(n)

print(f"n = {n_hex}")
print(f"\nBit length: {n.bit_length()}")

print("\n" + "="*70)
print("FACTORIZATION OPTIONS:")
print("="*70)
print("\n1. Try factordb.com manually:")
print(f"   http://factordb.com/index.php?query={n_hex[2:]}")  # Remove '0x' prefix

print("\n2. Use online tools:")
print("   - https://www.alpertron.com.ar/ECM.HTM")
print("   - http://factordb.com")

print("\n3. If you have sage installed, try:")
print(f"   sage: factor({n_hex})")

print("\n4. If you have yafu/msieve:")
print(f"   yafu \"factor({n_hex})\"")

print("\n5. Try primefac Python library:")
print("   pip install primefac")
print(f"   python -c 'import primefac; print(list(primefac.primefac({n_hex})))'")

print("\n" + "="*70)
print("\nAttempting primefac if available...")
print("="*70)

try:
    import primefac
    print("\n[*] primefac is installed. Attempting factorization...")
    print("[!] This may take a very long time for 2048-bit RSA modulus...")
    print("[!] Press Ctrl+C to cancel\n")
    
    factors = list(primefac.primefac(n))
    
    if len(factors) >= 2:
        print(f"\n[+] SUCCESS! Found factors:")
        for i, f in enumerate(factors):
            print(f"  Factor {i+1}: {f}")
        
        if len(factors) == 2:
            p, q = factors
            print(f"\np = {p}")
            print(f"q = {q}")
            print(f"\nYou can now use these factors in the solve script!")
    else:
        print(f"\n[!] Unexpected number of factors: {factors}")
        
except ImportError:
    print("\n[!] primefac not installed.")
    print("    Install with: pip install primefac")
except KeyboardInterrupt:
    print("\n\n[!] Factorization cancelled by user.")
except Exception as e:
    print(f"\n[!] Error during factorization: {e}")

print("\n" + "="*70)
print("ALTERNATIVE APPROACH:")
print("="*70)
print("\nIf standard factorization fails, the '2022 optimization' might refer to:")
print("1. A specific vulnerability in the quaternion construction")
print("2. Weak parameter generation (p, q with special form)")
print("3. A mathematical breakthrough that makes this easier")
print("\nWithout more context about the specific paper/method, ")
print("we may need to:")
print("- Research 'Quaternion RSA 2022' papers")
print("- Look for recent cryptanalysis of quaternion-based schemes")
print("- Check if this is a known CTF challenge with writeups")
