#!/usr/bin/env python3
import socket
from time import sleep
from hashlib import sha256
from Crypto.Util.number import bytes_to_long, inverse

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        if self.x is None: return other
        if other.x is None: return self
        if self.x == other.x:
            if self.y == other.y:
                s = (3 * self.x * self.x * inverse(2 * self.y, p)) % p
            else:
                return Point(None, None)
        else:
            s = ((other.y - self.y) * inverse((other.x - self.x) % p, p)) % p
        x = (s * s - self.x - other.x) % p
        y = (s * (self.x - x) - self.y) % p
        return Point(x, y)
    def __rmul__(self, scalar):
        if scalar == 0: return Point(None, None)
        result, addend = Point(None, None), self
        while scalar:
            if scalar & 1: result = result + addend
            addend, scalar = addend + addend, scalar >> 1
        return result

def h(msg): return bytes_to_long(sha256(msg).digest()) % n

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("nonce-rewind.ctf.fr13nds.team", 31337))
sock.recv(4096)

# Get public key
sock.sendall(b"pubkey\n")
sleep(0.5)
pubkey_resp = sock.recv(4096).decode()
Qx_session = Qy_session = None
for line in pubkey_resp.split('\n'):
    if 'Qx =' in line or 'Qx=' in line:
        try:
            Qx_session = int(line.split('=')[1].strip(), 16)
        except:
            pass
    if 'Qy =' in line or 'Qy=' in line:
        try:
            Qy_session = int(line.split('=')[1].strip(), 16)
        except:
            pass

if Qx_session and Qy_session:
    print(f"[*] Session public key:")
    print(f"    Qx = {Qx_session:064x}")
    print(f"    Qy = {Qy_session:064x}")
    print()
else:
    print("[-] Could not parse public key, continuing anyway...")

sigs = []
for i in range(1, 21):
    sock.sendall(f"sign {i:04x}\n".encode())
    sleep(0.3)
    data = sock.recv(4096).decode()
    r = s = None
    for line in data.split('\n'):
        if 'r =' in line: r = int(line.split('=')[1].strip(), 16)
        if 's =' in line: s = int(line.split('=')[1].strip(), 16)
    if r and s:
        sigs.append((i, r, s, h(bytes.fromhex(f"{i:04x}"))))

print(f"[+] Collected {len(sigs)} signatures")

# Find reuse
for i in range(len(sigs)):
    for j in range(i+1, len(sigs)):
        if sigs[i][1] == sigs[j][1]:  # same r
            print(f"[+] Nonce reuse: sig{sigs[i][0]} and sig{sigs[j][0]}")
            
            _, r, s1, h1 = sigs[i]
            _, _, s2, h2 = sigs[j]
            
            k = ((h1 - h2) * inverse((s1 - s2) % n, n)) % n
            d = ((s1 * k - h1) * inverse(r, n)) % n
            
            print(f"[+] k = {k:064x}")
            print(f"[+] d = {d:064x}")
            
            # Verify d against session public key if we have it
            if Qx_session and Qy_session:
                G = Point(Gx, Gy)
                Q_calc = d * G
                print(f"\n[*] Verification:")
                print(f"    Computed Qx = {Q_calc.x:064x}")
                print(f"    Session  Qx = {Qx_session:064x}")
                print(f"    Match: {Q_calc.x == Qx_session and Q_calc.y == Qy_session}")
                
                if Q_calc.x != Qx_session or Q_calc.y != Qy_session:
                    print("[-] Private key doesn't match session public key!")
                    sock.sendall(b"quit\n")
                    sock.close()
                    continue
            
            # Sign admin
            admin = bytes.fromhex("676976655f6d655f666c6167")
            k_sign = 0xcafe1234567890abcdefcafe1234567890abcdefcafe1234567890abcdef1234
            G = Point(Gx, Gy)
            R = k_sign * G
            r_a = R.x % n
            s_a = (inverse(k_sign, n) * (h(admin) + r_a * d)) % n
            
            cmd = f"verify 676976655f6d655f666c6167 {r_a:064x} {s_a:064x}\n"
            print(f"[*] Sending: {cmd.strip()}")
            sock.sendall(cmd.encode())
            sleep(1)
            resp = sock.recv(8192).decode()
            
            print("[*] Raw response:")
            print(repr(resp))
            print("\n[*] Response:")
            print(resp)
            
            if "fr13nds{" in resp:
                print("\n[SUCCESS]")
                for line in resp.split('\n'):
                    if "fr13nds{" in line:
                        print(line)
            
            sock.sendall(b"quit\n")
            sock.close()
            exit(0)

print("[-] No reuse found")
sock.sendall(b"quit\n")
sock.close()
