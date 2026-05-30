#!/usr/bin/env sage
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

# Parameters from val.txt
p = 129403459552990578380563458675806698255602319995627987262273876063027199999999
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]
G_u = [95640493847532285274015733349271558012724241405617918614689663966283911276425, 1]
G_v = [23400917335266251424562394829509514520732985938931801439527671091919836508525]
Q_u = [34277069903919260496311859860543966319397387795368332332841962946806971944007, 343503204040841221074922908076232301549085995886639625441980830955087919004, 1]
Q_v = [102912018107558878490777762211244852581725648344091143891953689351031146217393, 65726604025436600725921245450121844689064814125373504369631968173219177046384]
enc_flag = bytes.fromhex("f6ca1f88bdb8e8dda17861b91704523f914564888c7138c24a3ab98902c10de5")

# Create the hyperelliptic curve
Fp = GF(p)
R = PolynomialRing(Fp, 'x')
x = R.gen()
f = R(f_coeffs)

print(f"[+] Creating hyperelliptic curve y^2 = f(x)")
print(f"[+] Degree of f: {f.degree()}")

# Create the hyperelliptic curve
H = HyperellipticCurve(f)
J = H.jacobian()(Fp)

print(f"[+] Curve created successfully")

# Convert Mumford coordinates to Jacobian points
# For genus 2, points are represented as (u(x), v(x)) where u is degree <= 2 and v is degree <= 1
# G_u = [a, b] means u(x) = x^2 + a*x + b (assuming leading coefficient is 1)
# G_v = [c] means v(x) = c

# For G: u(x) = x^2 + G_u[0]*x + G_u[1], v(x) = G_v[0]
u_G = x^2 + Fp(G_u[0])*x + Fp(G_u[1])
v_G = Fp(G_v[0])
G = J([u_G, v_G])

print(f"[+] Point G created: {G}")

# For Q: u(x) = x^3 + Q_u[0]*x^2 + Q_u[1]*x + Q_u[2]
# But wait, Q_u has 3 elements, which suggests degree 3 polynomial
# However, for genus 2, u should be degree <= 2
# Let's check if this is actually degree 2 (leading coefficient might be implicit)

# Try interpreting Q as degree 2: u(x) = x^2 + Q_u[0]*x + Q_u[1] (ignoring Q_u[2] for now)
# v(x) = Q_v[0]*x + Q_v[1]

u_Q = x^2 + Fp(Q_u[0])*x + Fp(Q_u[1])
v_Q = Fp(Q_v[0])*x + Fp(Q_v[1])
Q = J([u_Q, v_Q])

print(f"[+] Point Q created: {Q}")

# Now solve the discrete log problem: Q = k*G
print(f"[+] Computing discrete log to find k such that Q = k*G...")

try:
    k = G.discrete_log(Q)
    print(f"[+] Found k = {k}")
    
    # Derive AES key from k
    key = hashlib.sha256(long_to_bytes(int(k))).digest()[:16]
    
    # Decrypt the flag
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(enc_flag)
    
    print(f"\n[+] FLAG: {flag.decode()}")
    
except Exception as e:
    print(f"[-] Error during discrete log: {e}")
    print(f"[-] Trying alternative interpretation...")
    
    # Maybe the curve is weak - let's check the order
    print(f"[+] Computing order of G...")
    order_G = G.order()
    print(f"[+] Order of G: {order_G}")
    print(f"[+] Factorization: {factor(order_G)}")
