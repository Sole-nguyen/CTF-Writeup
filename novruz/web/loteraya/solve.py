#!/usr/bin/env python3
import argparse
import base64
import hashlib
import http.cookiejar
import json
import re
import sys
import urllib.request


def rd_len(buf, p):
    l = buf[p]
    p += 1
    if l < 0x80:
        return l, p
    n = l & 0x7F
    l = int.from_bytes(buf[p:p + n], "big")
    p += n
    return l, p


def rd_tlv(buf, p):
    t = buf[p]
    p += 1
    l, p = rd_len(buf, p)
    v = buf[p:p + l]
    p += l
    return t, v, p


def parse_nd_from_pkcs8_pem(pem_key):
    der = base64.b64decode("".join(line for line in pem_key.splitlines() if "---" not in line))
    t, outer, _ = rd_tlv(der, 0)
    if t != 0x30:
        raise ValueError("Invalid PKCS#8 key")

    p = 0
    _, _, p = rd_tlv(outer, p)  # version
    _, _, p = rd_tlv(outer, p)  # algorithm identifier
    t, pk_octets, _ = rd_tlv(outer, p)
    if t != 0x04:
        raise ValueError("Invalid PKCS#8 privateKey field")

    t, rsa_seq, _ = rd_tlv(pk_octets, 0)
    if t != 0x30:
        raise ValueError("Invalid RSAPrivateKey")

    vals = []
    p = 0
    while p < len(rsa_seq):
        t, iv, p = rd_tlv(rsa_seq, p)
        if t != 0x02:
            break
        vals.append(int.from_bytes(iv, "big", signed=False))

    if len(vals) < 4:
        raise ValueError("Incomplete RSA key")

    n = vals[1]
    d = vals[3]
    return n, d


def mgf1(seed, out_len):
    out = b""
    c = 0
    while len(out) < out_len:
        out += hashlib.sha1(seed + c.to_bytes(4, "big")).digest()
        c += 1
    return out[:out_len]


def oaep_unpad_sha1(encoded_message):
    hlen = 20
    if len(encoded_message) < 2 * hlen + 2:
        raise ValueError("Encoded message too short")

    y = encoded_message[0]
    masked_seed = encoded_message[1:1 + hlen]
    masked_db = encoded_message[1 + hlen:]

    seed = bytes(a ^ b for a, b in zip(masked_seed, mgf1(masked_db, hlen)))
    db = bytes(a ^ b for a, b in zip(masked_db, mgf1(seed, len(masked_db))))

    lhash = hashlib.sha1(b"").digest()
    if y != 0 or db[:hlen] != lhash:
        raise ValueError("Invalid OAEP block")

    idx = db.find(b"\x01", hlen)
    if idx < 0:
        raise ValueError("OAEP delimiter not found")

    return db[idx + 1:]


def solve(url, max_rounds=3000, verbose_every=100):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # Initialize one challenge to populate session cookies
    _ = json.loads(opener.open(url + "/generate-task", timeout=10).read().decode())

    for i in range(1, max_rounds + 1):
        session_cookie = next((c.value for c in cj if c.name == "session"), None)
        if not session_cookie:
            raise RuntimeError("Missing session cookie")

        state = json.loads(base64.b64decode(session_cookie))
        n, d = parse_nd_from_pkcs8_pem(state["key"])

        ciphertext = base64.b64decode(state["task"]["c"])
        k = (n.bit_length() + 7) // 8

        plaintext = b""
        for off in range(0, len(ciphertext), k):
            c_int = int.from_bytes(ciphertext[off:off + k], "big")
            em = pow(c_int, d, n).to_bytes(k, "big")
            plaintext += oaep_unpad_sha1(em)

        text = plaintext.decode("utf-8", "ignore")
        m = re.search(r"-?\d+", text)
        answer = m.group(0) if m else text.strip()

        req = urllib.request.Request(
            url + "/check-task",
            data=json.dumps({"input": answer}).encode(),
            headers={"Content-Type": "application/json"},
        )
        resp = json.loads(opener.open(req, timeout=10).read().decode())

        flag = resp.get("flag")
        if verbose_every and (i % verbose_every == 0 or flag):
            print(f"[+] round={i} answered={resp.get('answered')} success={resp.get('success')} flag={flag}")

        if flag:
            return flag

    return None


def main():
    parser = argparse.ArgumentParser(description="NovruzCTF loteraya solver")
    parser.add_argument("--url", default="http://95.111.234.103:2900", help="challenge base URL")
    parser.add_argument("--max-rounds", type=int, default=3000, help="maximum rounds to solve")
    parser.add_argument("--verbose-every", type=int, default=100, help="progress print interval")
    args = parser.parse_args()

    flag = solve(args.url.rstrip("/"), args.max_rounds, args.verbose_every)
    if flag:
        print(f"FLAG: {flag}")
        return 0

    print("[-] No flag found within max rounds")
    return 1


if __name__ == "__main__":
    sys.exit(main()) 