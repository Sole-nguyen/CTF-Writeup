#!/usr/bin/env sage
# Pohlig-Hellman attack on the hyperelliptic curve Jacobian
# Key insight: order(G) = p+1 which factors completely into small primes

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

p = 129403459552990578380563458675806698255602319995627987262273876063027199999999
f_coeffs = [87455262955769204408909693706467098277950190590892613056321965035180446006909, 12974562908961912291194866717212639606874236186841895510497190838007409517645, 11783716142539985302405554361639449205645147839326353007313482278494373873961, 55538572054380843320095276970494894739360361643073391911629387500799664701622, 124693689608554093001160935345506274464356592648782752624438608741195842443294, 52421364818382902628746436339763596377408277031987489475057857088827865195813, 50724784947260982182351215897978953782056750224573008740629192419901238915128]

Fp = GF(p)
R.<x> = PolynomialRing(Fp)
f = R(f_coeffs)

H = HyperellipticCurve(f)
J = H.jacobian()(Fp)

G_u = R([95640493847532285274015733349271558012724241405617918614689663966283911276425, 1])
G_v = R([23400917335266251424562394829509514520732985938931801439527671091919836508525])
G = J([G_u, G_v])

Q_u = R([34277069903919260496311859860543966319397387795368332332841962946806971944007, 343503204040841221074922908076232301549085995886639625441980830955087919004, 1])
Q_v = R([102912018107558878490777762211244852581725648344091143891953689351031146217393, 65726604025436600725921245450121844689064814125373504369631968173219177046384])
Q = J([Q_u, Q_v])

# The order of G is p+1, which is B-smooth
N = p + 1
# N = 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4

print(f"[+] N = p+1 = {N}")
print(f"[+] Factoring N: {factor(N)}")

# Verify N is the order of G
print("\n[+] Verifying N * G == identity...")
if N * G == J(0):
    print("[+] Confirmed: N * G = 0")
else:
    print("[-] WARNING: N * G != 0, order might be different!")

# Pohlig-Hellman: for each prime q^e | N, find k mod q^e
factor_list = list(factor(N))
print(f"\n[+] Factor list: {factor_list}")

def pohlig_hellman_prime_power(G, Q, J, q, e, N):
    """Solve k*G = Q for k mod q^e, where order(G) = N."""
    # g0 has order exactly q
    g0 = (N // q) * G
    
    k_partial = 0
    for i in range(e):
        # Compute R_i = Q - k_partial * G
        # Use (N - k_partial) * G instead of negation to avoid issues
        if k_partial == 0:
            R_i = Q
        else:
            neg_partial_G = (N - k_partial) * G  # = -k_partial * G
            R_i = Q + neg_partial_G
        
        # h_i should be in the subgroup of order q
        coeff = N // (q^(i+1))
        h_i = coeff * R_i
        
        # Find x_i in [0, q) such that x_i * g0 == h_i
        found = False
        cur = J(0)
        for x_i in range(q):
            if cur == h_i:
                k_partial += x_i * (q^i)
                found = True
                break
            cur = cur + g0
        
        if not found:
            print(f"    [!] Could not find x_{i} for prime {q}^{e}")
            return None
    
    return k_partial

print("\n[+] Starting Pohlig-Hellman...")
remainders = []
moduli = []

for q, e in factor_list:
    q_e = q^e
    print(f"[+] Solving DLP mod {q}^{e} = {q_e}...", end=' ', flush=True)
    
    k_mod = pohlig_hellman_prime_power(G, Q, J, q, e, N)
    
    if k_mod is not None:
        print(f"k ≡ {k_mod} (mod {q_e})")
        remainders.append(int(k_mod))
        moduli.append(int(q_e))
    else:
        print(f"FAILED!")
        break

if len(remainders) == len(factor_list):
    k = CRT(remainders, moduli)
    print(f"\n[+] k = {k}")
    
    # Verify
    print("[+] Verifying k * G == Q...")
    if k * G == Q:
        print("[+] VERIFIED!")
    else:
        print("[-] Verification failed, trying adjustments...")
        found_k = False
        for adj in range(1, N // max(moduli) + 2):
            for sign in [1, -1]:
                k_try = k + sign * adj * prod(moduli)
                if 0 <= k_try < N and k_try * G == Q:
                    k = k_try
                    print(f"[+] Adjusted k = {k}")
                    found_k = True
                    break
            if found_k:
                break
    
    # Decrypt the flag
    print("\n[+] Decrypting flag...")
    enc_flag = bytes.fromhex("f6ca1f88bdb8e8dda17861b91704523f914564888c7138c24a3ab98902c10de5")
    
    # Try different key derivations
    for desc, key in [
        ("SHA256(long_to_bytes(k))[:16]", hashlib.sha256(long_to_bytes(int(k))).digest()[:16]),
        ("SHA256(str(k).encode())[:16]",  hashlib.sha256(str(k).encode()).digest()[:16]),
        ("long_to_bytes(k)[:16]",         long_to_bytes(int(k))[:16].rjust(16, b'\x00')),
    ]:
        try:
            cipher = AES.new(key, AES.MODE_ECB)
            flag = cipher.decrypt(enc_flag)
            if b'BITS' in flag or b'CTF' in flag or b'flag' in flag or b'{' in flag:
                print(f"\n[!!!] FLAG FOUND (key={desc}):")
                print(flag.decode(errors='replace'))
                break
            else:
                print(f"    key={desc}: {flag.hex()} (not a flag)")
        except Exception as ex:
            print(f"    key={desc}: error {ex}")
else:
    print(f"\n[-] Pohlig-Hellman incomplete ({len(remainders)}/{len(factor_list)} primes solved)")
