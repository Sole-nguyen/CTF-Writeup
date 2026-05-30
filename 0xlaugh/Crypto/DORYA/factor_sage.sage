from sage.all import *

n = 118636480445922997414990601093376262738873200793785339179564817109865454031931486586508946517137468038918549130611281608407631797608189160613009202727333210449589813079603946610204369133692321049079826961684843062183608289281070542325771713618963848998628576932902235933106794937930673264643682434933057492433

print(f"Attempting to factor n ({n.nbits()} bits)...")
print(f"n = {n}")
print()

# Try various factorization methods
print("Trying factor()...")
try:
    factors = factor(n, verbose=True)
    print(f"\nFactors: {factors}")
except KeyboardInterrupt:
    print("\nFactorization interrupted")
except Exception as ex:
    print(f"\nFactor failed: {ex}")
