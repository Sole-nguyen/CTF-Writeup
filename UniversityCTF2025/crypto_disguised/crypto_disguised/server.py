import json, hashlib, os
from utils import _msc, _ek, b2m, m2b, B
from Crypto.Util.Padding import pad

class HearthProtocol:
    def __init__(self, cipher):
        self.cipher = cipher
        self.admin_uid = 0
        self.uid = 1

    def login(self, uid, username, token):
        snowprint = hashlib.shake_256(self.cipher.KEY + username + str(uid).encode()).digest(64)
        real_token = self.cipher.encrypt(json.dumps({"s": snowprint.hex(), "i": uid}).encode())
        if real_token == token:
            if uid == self.admin_uid and username == b'TinselwickAdmin':
                return { "success": f"Warm greetings, admin! Your Starshard scroll: {open('flag.txt').read()}" }
            else:
                return { "success": f"Welcome {username.decode()}! No Starshard scrolls for you today." }
        else:
            return { "error": "Frostbitten session token. Identity unclear." }

    def register(self, username):
        if self.uid >= 32:
            return { "error": "The Hearth Registry is full for now... try again after the solstice." }
        snowprint = hashlib.shake_256(self.cipher.KEY + username + str(self.uid).encode()).digest(64)
        token = self.cipher.encrypt(json.dumps({"s": snowprint.hex(), "i": self.uid}).encode())
        self.uid += 1
        return { "token": token.hex() }

class SnowCipher:
    def __init__(self, key):
        self.KEY = key
    
    def _sb(self, s, b=B):
        return [[b[val] for val in row] for row in s]

    def _sr(self, s):
        res = [s[i].copy() for i in range(4)]
        res[0][1], res[1][1], res[2][1], res[3][1] = res[1][1], res[2][1], res[3][1], res[0][1]
        res[0][2], res[1][2], res[2][2], res[3][2] = res[2][2], res[3][2], res[0][2], res[1][2]
        res[0][3], res[1][3], res[2][3], res[3][3] = res[3][3], res[0][3], res[1][3], res[2][3]
        return res

    def _mc(self, s):
        return [_msc(s[i].copy()) for i in range(4)]

    def _ark(self, s, k):
        return [[t[0] ^ t[1] for t in list(zip(row[0], row[1]))] for row in zip(s, k)]

    def encrypt_block(self, block):
        rk = _ek(self.KEY)
        s = b2m(block)
        s = self._ark(s, rk[0])
        s = self._sb(s)
        s = self._sr(s)
        s = self._mc(s)
        s = self._ark(s, rk[1])
        return m2b(s)
    
    def encrypt(self, m):
        plaintext = pad(m, 16)
        return b''.join(self.encrypt_block(plaintext[i:i+16]) for i in range(0, len(plaintext), 16))

prot = HearthProtocol(SnowCipher(os.urandom(32)))

while True:
    print("[1] Request Hearth Token")
    print("[2] Authenticate with Hearth Token")
    print("[3] Leave Frostgate")

    choice = input("> ").strip()

    if choice == "1":
        username = input("Enter username: ").strip().encode()
        response = prot.register(username)
    elif choice == "2":
        try:
            uid = int(input("Enter UID: ").strip())
        except ValueError:
            print('[-] UID must be numeric.')
            continue
        username = input("Enter username: ").strip().encode()
        token_hex = input("Enter token (hex): ").strip()
        token = bytes.fromhex(token_hex)
        response = prot.login(uid, username, token)
    elif choice == "3":
        print("The Frostgate closes... stay warm.")
        break
    else:
        print("Try a valid option, snowflake.")
        continue

    print(json.dumps(response))