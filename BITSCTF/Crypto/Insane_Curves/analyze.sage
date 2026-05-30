#!/usr/bin/env sage

# Let me try a simpler approach - check if we can work this out differently
# Parameters from val.txt
p = 129403459552990578380563458675806698255602319995627987262273876063027199999999

print(f"[+] Prime p: {p}")
print(f"[+] Checking if p is prime: {is_prime(p)}")
print(f"[+] p bit length: {p.nbits()}")

# Let's factor p-1 and p+1 to see if there's something interesting
print("\n[+] Factoring p-1:")
print(factor(p-1))

print("\n[+] Factoring p+1:")
print(factor(p+1))

# Check the f_coeffs structure
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

print(f"\n[+] Number of coefficients: {len(f_coeffs)}")

# Create field and polynomial
Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

print(f"[+] Polynomial f: degree {f.degree()}")

# Let's try to see if f factors
print("\n[+] Attempting to factor f(x)...")
try:
    factors_f = f.factor()
    print(f"[+] Factorization of f: {factors_f}")
    
    if len(factors_f) > 1:
        print("\n[!!!] The polynomial f(x) factors! This might be the weakness!")
        for factor_poly, mult in factors_f:
            print(f"  Factor: {factor_poly}, multiplicity: {mult}, degree: {factor_poly.degree()}")
except Exception as e:
    print(f"[-] Could not factor: {e}")
