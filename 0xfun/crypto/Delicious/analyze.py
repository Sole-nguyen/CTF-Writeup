from Crypto.Util.number import *
from sympy import factorint

# Parse the output
samples = [
    (227293414901, 1559214942312, 3513364021163),
    (2108076514529, 1231299005176, 2627609083643),
    (1752240335858, 1138499826278, 2917520243087),
    (1564551923739, 283918762399, 2602533803279),
    (1809320390770, 700655135118, 2431482961679),
    (1662077312271, 354214090383, 2820691962743),
    (474213905602, 1149389382916, 3525049671887),
    (2013522313912, 2559608094485, 2679851241659),
]

print("Analyzing primes...")
for idx, (g, h, p) in enumerate(samples):
    print(f"\nSample #{idx+1}:")
    print(f"p = {p} ({p.bit_length()} bits)")
    
    # Check if p is prime
    from sympy import isprime
    print(f"Is p prime? {isprime(p)}")
    
    # Try to factor p-1
    print(f"Trying to factor p-1...")
    try:
        factors = factorint(p-1, limit=10**7)
        print(f"p-1 factors: {factors}")
        
        # Check if smooth
        max_factor = max(factors.keys())
        print(f"Max prime factor: {max_factor} ({max_factor.bit_length()} bits)")
        
        if max_factor < 2**30:
            print("  -> Smooth! Can use Pohlig-Hellman")
    except Exception as e:
        print(f"  Factorization failed: {e}")
