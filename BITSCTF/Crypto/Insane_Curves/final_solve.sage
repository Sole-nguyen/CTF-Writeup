#!/usr/bin/env sage

# Exploit for Insane Curves CTF Challenge
# The key insight: p+1 is extremely smooth, making the DLP solvable via Pohlig-Hellman

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

p = 129403459552990578380563458675806698255602319995627987262273876063027199999999
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

print("[+] Setting up hyperelliptic curve...")
Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

H = HyperellipticCurve(f)
J = H.jacobian()(Fp)

print("[+] Creating Jacobian points from Mumford representation...")

# G point
G_u = R([95640493847532285274015733349271558012724241405617918614689663966283911276425, 1])
G_v = R([23400917335266251424562394829509514520732985938931801439527671091919836508525])
G = J([G_u, G_v])
print(f"[+] G created: {G}")

# Q point  
Q_u = R([34277069903919260496311859860543966319397387795368332332841962946806971944007, 343503204040841221074922908076232301549085995886639625441980830955087919004, 1])
Q_v = R([102912018107558878490777762211244852581725648344091143891953689351031146217393, 65726604025436600725921245450121844689064814125373504369631968173219177046384])
Q = J([Q_u, Q_v])
print(f"[+] Q created: {Q}")

print("\n[+] Key insight: p+1 is extremely smooth!")
print(f"[+] p+1 = 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4")

# For genus 2 curves, the Jacobian order is approximately (p+1)^2
# Try various candidates near (p+1)^2
p_plus_1 = p + 1

print("\n[+] Estimating Jacobian order based on Hasse-Weil bound...")
print("[+] For genus g=2: |#J(F_p) - (p+1)^2| <= 4*g*sqrt(p)")

# Try candidate orders
base_order = p_plus_1 * p_plus_1

print(f"\n[+] Testing candidate orders near (p+1)^2...")

# Common patterns for genus 2 Jacobians
candidates = [
    base_order,
    base_order + 2*p_plus_1,
    base_order - 2*p_plus_1,
    p_plus_1^2,
]

# Also try with small adjustments
for i in range(-10, 11):
    candidates.append(base_order + i * p_plus_1)

k_found = None

for idx, candidate_order in enumerate(candidates[:30]):  # Limit checks
    if idx % 5 == 0:
        print(f"[+] Testing candidate {idx}...")
    
    try:
        # Check if both points have this order
        if candidate_order * G == J(0) and candidate_order * Q == J(0):
            print(f"\n[!!! Both G and Q annihilated by order {candidate_order}")
            print("[+] Attempting discrete log with Pohlig-Hellman...")
            
            try:
                k = discrete_log(Q, G, candidate_order, operation='+')
                print(f"\n[!!!] SUCCESS! Found k = {k}")
                k_found = k
                break
            except Exception as e:
                print(f"    DLP failed: {e}")
                continue
    except:
        continue

if k_found is None:
    # Try without specifying order - let Sage figure it out
    print("\n[+] Trying discrete_log without specifying order...")
    try:
        k_found = discrete_log(Q, G, operation='+')
        print(f"\n[!!!] SUCCESS! Found k = {k_found}")
    except Exception as e:
        print(f"[-] Failed: {e}")

if k_found is not None:
    print("\n[+] Decrypting flag...")
    key = hashlib.sha256(long_to_bytes(int(k_found))).digest()[:16]
    enc_flag = bytes.fromhex("f6ca1f88bdb8e8dda17861b91704523f914564888c7138c24a3ab98902c10de5")
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(enc_flag)
    
    print(f"\n{'='*60}")
    print(f"FLAG: {flag.decode()}")
    print(f"{'='*60}")
else:
    print("\n[-] Could not find k")
