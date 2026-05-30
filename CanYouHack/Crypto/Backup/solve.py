from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fpylll import CVP, IntegerMatrix, LLL


def recover_flag():
    q = 14506767387559045101601535119277212163585226958374735478472887178858388862703

    m1 = "Hi! Can you store the encrypted flag for me for a second? I will need it later."
    s11 = 13205737753786145631452557588406232353600988478055542460813697878122967446578
    s12 = 13958963271047914149117054426506396333295463042827503250264570272717038726261
    R1 = 10975523781415982714076120021487634912523174941670197886572626886997379163321

    ct_hex = (
        "2ccb051234f87b7786c829e31ed2539d62f93c39da366b5d8a74890960c1fc38"
        "d33b6fbd804fb5aa555e3e2928e1e06c564956eb2f320dde516ababeb71d525b"
        "9069538a7abc76cb3c94b7955654c041"
    )
    m2 = "Here's the flag: " + ct_hex
    s21 = 9179666933751539920348309886276181210967936400505991858211575258442611791125
    s22 = 9320577211559440207387497803168253329006224294550698569339457019099653730952
    R2 = 27255728356841764650107110242922607077260936240190827215432957010403469676198

    def h(inputs):
        msg = "".join(map(str, inputs)).encode()
        return int(sha256(msg).hexdigest(), 16) % q

    h1 = h([m1, R1])
    h2 = h([m2, R2])
    t1 = (s11 - s12) % q
    t2 = (s21 - s22) % q

    inv_h1 = pow(h1, -1, q)
    c = (h2 * inv_h1) % q
    a = (t2 - (h2 * t1 % q) * inv_h1) % q

    lattice = IntegerMatrix(2, 2)
    lattice[0, 0] = q
    lattice[0, 1] = 0
    lattice[1, 0] = c
    lattice[1, 1] = 1
    LLL.reduction(lattice)

    target = (-a, 0)
    closest = CVP.closest_vector(lattice, target)
    e1 = int(closest[1] - target[1])
    if e1 > q // 2:
        e1 -= q

    d = ((t1 - e1) % q) * inv_h1 % q

    key = (int(sha256(str(d).encode()).hexdigest(), 16) % q).to_bytes(32, "big")
    iv = bytes.fromhex(ct_hex[:32])
    ct = bytes.fromhex(ct_hex[32:])
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    return unpad(pt, 16).decode()


if __name__ == "__main__":
    print(recover_flag())
