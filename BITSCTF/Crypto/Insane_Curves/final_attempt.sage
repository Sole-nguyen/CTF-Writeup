#!/usr/bin/env sage

# Final attempt: Since f factors, we can exploit the product structure
# The Jacobian J decomposes. Let me use a practical attack.

p = 129403459552990578380563458675806698255602319995627987262273876063027199999999
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

print("[+] Working with hyperelliptic curve")
factors = f.factor()

# Get the quadratic factors (there should be 3)
quad_factors = [factors[i][0] for i in range(len(factors)) if factors[i][0].degree() == 2]
print(f"[+] Found {len(quad_factors)} quadratic factors")

f1 = quad_factors[0]
f2 = quad_factors[1]
f3 = quad_factors[2]

print(f"[+] f1 = {f1}")
print(f"[+] f2 = {f2}")
print(f"[+] f3 = {f3}")

# For each quadratic y^2 = ai*x^2 + bi*x + ci, find the roots
# This gives us points on genus 0 curves

# Try to find roots of each factor
print("\n[+] Finding roots of factors...")
for i, fi in enumerate([f1, f2, f3]):
    roots_fi = fi.roots()
    print(f"f{i+1} roots: {roots_fi}")

# Since f splits completely into quadratics, let me check if any of them split further
# If f = f1*f2*f3 where each fi = (x-ai)(x-bi), then we have 6 roots total

all_roots = []
for fi in [f1, f2, f3]:
    roots = fi.roots()
    for root, mult in roots:
        all_roots.append(root)

print(f"\n[+] Found {len(all_roots)} roots total")

if len(all_roots) == 6:
    print("[!!!] f splits completely over Fp!")
    print(f"[+] Roots: {all_roots[:3]}...") 
    
    # When genus 2 curve is completely split, the Jacobian is trivial/simple
    # The DLP should be easy!
    
    # However, we still need to properly construct the points
    # Let me try a different tactic: use magma or write to file for external solving

print("\n[+] Since we have complete factorization, let me try finding actual points...")
print(f"[+] p+1 factorization: 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4")

# The smooth order means even if DLP is not trivial, Pohlig-Hellman works
# But we need to be able to construct the points first

# Let me try one more thing - maybe the coordinates are Kummer coordinates
# Or perhaps we need to use a different library

print("\n[+] Attempting to create curve with Sage...")
H = HyperellipticCurve(f)
print(f"[+] Curve: {H}")

# Check the genus
print(f"[+] Genus: {H.genus()}")

# Get the Jacobian
J = H.jacobian()(Fp)
print(f"[+] Jacobian created")

# Try creating a random point to see the expected format
print("\n[+] Trying to create a random point...")
try:
    random_pt = J.random_element()
    print(f"[+] Random point: {random_pt}")
    print(f"[+] Type: {type(random_pt)}")
except Exception as e:
    print(f"[-] Could not create random point: {e}")

# Let me manually try to find a valid Mumford representation
print("\n[+] Manually searching for valid divisor...")

# For  genus 2, a point in Mumford form is [u(x), v(x)] where:
# - u is monic of degree <= 2
# - v has degree < deg(u)  
# - v^2 ≡ f (mod u)

# Let's try u(x) = x - r for each root r
for i, root in enumerate(all_roots[:3]):
    u_test = x - root
    # Find v such that v^2 ≡ f (mod u)
    # v^2 ≡ f(root) (mod x-root)
    # So v = ±sqrt(f(root))
    
    f_at_root = f(root)
    print(f"\n[+] Testing root {i+1}: {root}")
    print(f"    f(root) = {f_at_root}")
    
    if f_at_root == 0:
        print(f"    Root is on curve! v = 0")
        try:
            pt = J([u_test, R(0)])
            print(f"    Created point: {pt}")
        except Exception as e:
            print(f"    Error: {e}")
