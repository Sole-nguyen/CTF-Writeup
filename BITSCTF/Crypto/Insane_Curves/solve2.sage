#!/usr/bin/env sage

# The key insight: f(x) factors completely means the Jacobian is weak
# Let's compute the order and use Pohlig-Hellman

p = 129403459552990578380563458675806698255602319995627987262273876063027199999999

# Looking at p+1 factorization, it's VERY smooth!
# 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4

# For genus 2 hyperelliptic curves, |#J(F_p) - (p+1)^2| <= 2g * 2^g * p^g
# which means #J(F_p) is close to (p+1)^2

# Given the structure, the order likely inherits the smooth factorization
# Let's work with this

f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

print("[+] Creating hyperelliptic curve...")
H = HyperellipticCurve(f)
J = H.jacobian()(Fp)

print("[+] Curve created")

# Construct points - we need to be more careful about the format
# Looking at the data: G_u has 2 coeffs, G_v has 1 coeff
# Q_u has 3 coeffs, Q_v has 2 coeffs

# For Mumford representation [u, v]:
# - u is monic of degree <= g (genus), so for genus 2, degree <= 2
# - v has degree < deg(u)
# - v^2 ≡ f (mod u)

# G: u(x) = x^2 + c1*x + c0 (monic), v(x) = d0
G_u_poly = x^2 + Fp(95640493847532285274015733349271558012724241405617918614689663966283911276425)*x + Fp(1)
G_v_poly = Fp(23400917335266251424562394829509514520732985938931801439527671091919836508525)

print("[+] Trying to create point G...")
print(f"    u_G = {G_u_poly}")
print(f"    v_G = {G_v_poly}")

# Verify the Mumford condition: v^2 ≡ f (mod u)
v_squared = R((G_v_poly)^2)
f_mod_u = f % G_u_poly
v_sq_mod_u = v_squared % G_u_poly
print(f"    v^2 mod u = {v_sq_mod_u}")
print(f"    f mod u = {f_mod_u}")
print(f"    Valid? {v_sq_mod_u == f_mod_u}")

if v_sq_mod_u == f_mod_u:
    G = J([G_u_poly, G_v_poly])
    print("[+] Point G created successfully!")
    
    # Now for Q - it seems to have different format
    # Q_u has 3 elements [a, b, c] - maybe represents x^2 + a*x + b, and c is for something else?
    # Let's try interpreting as: u(x) = x^2 + Q_u[0]*x + Q_u[1]
    
    Q_u_poly = x^2 + Fp(34277069903919260496311859860543966319397387795368332332841962946806971944007)*x + Fp(343503204040841221074922908076232301549085995886639625441980830955087919004)
    Q_v_poly = Fp(102912018107558878490777762211244852581725648344091143891953689351031146217393)*x + Fp(65726604025436600725921245450121844689064814125373504369631968173219177046384)
    
    print("\n[+] Trying to create point Q...")
    print(f"    u_Q = {Q_u_poly}")
    print(f"    v_Q = {Q_v_poly}")
    
    v_squared_Q = R((Q_v_poly)^2)
    f_mod_u_Q = f % Q_u_poly
    v_sq_mod_u_Q = v_squared_Q % Q_u_poly
    print(f"    v^2 mod u = {v_sq_mod_u_Q}")
    print(f"    f mod u = {f_mod_u_Q}")
    print(f"    Valid? {v_sq_mod_u_Q == f_mod_u_Q}")
    
    if v_sq_mod_u_Q == f_mod_u_Q:
        Q = J([Q_u_poly, Q_v_poly])
        print("[+] Point Q created successfully!")
        
        # Now solve discrete log
        print("\n[+] Computing order of G...")
        order_G = G.order()
        print(f"[+] Order of G: {order_G}")
        print(f"[+] Factorization: {factor(order_G)}")
        
        print("\n[+] Solving discrete log: Q = k*G...")
        k = G.discrete_log(Q)
        print(f"\n[+] Found k = {k}")
        
        # Save for decryption
        with open('key.txt', 'w') as f:
            f.write(str(k))
        print("[+] Key saved to key.txt")
    else:
        print("[-] Q is not a valid point")
else:
    print("[-] G is not a valid point")
