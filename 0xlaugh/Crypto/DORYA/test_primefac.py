from Crypto.Util.number import long_to_bytes, inverse
import primefac

# Load one modulus to try factoring
n = 118636480445922997414990601093376262738873200793785339179564817109865454031931486586508946517137468038918549130611281608407631797608189160613009202727333210449589813079603946610204369133692321049079826961684843062183608289281070542325771713618963848998628576932902235933106794937930673264643682434933057492433
c = 85245911405166612359858091783054881795731056510112601911606301947571291279154016120081154880734315849097920140655909625901956711124236650532809801624318091766720604993267558138969488943103164261298759313955791149617121427046412247417646539270303396702168129740700024701970789126704213360948160444564937912612

e = 7

print(f"Trying to factor n (1024 bits)...")
print(f"n = {n}")

try:
    factors = list(primefac.primefac(n))
    print(f"\nFactors found: {factors}")
    
    if len(factors) == 2:
        p, q = factors
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"Verification: p*q == n? {p*q == n}")
        
        # Calculate phi and decrypt
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)
        
        print(f"\nDecrypted m = {m}")
        flag = long_to_bytes(m)
        print(f"Flag (if this is first round): {flag}")
        
except Exception as ex:
    print(f"Factorization failed: {ex}")
