#!/usr/bin/env python3
import socket, re, hashlib, random, sys

HOST = "challenges.ctf.hackastra.tech"
PORT = 32459
N = 256
MASK = (1 << N) - 1

try:
    from Crypto.Cipher import AES
    def aes_cbc_decrypt(key, iv, ct):
        return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
except Exception:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    def aes_cbc_decrypt(key, iv, ct):
        dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
        return dec.update(ct) + dec.finalize()


def lfsr_stream(seed, taps, n=N):
    """Return first n output bits packed as an int; bit i is output at time i."""
    st = [(seed >> (15 - i)) & 1 for i in range(16)]
    out = 0
    for i in range(n):
        if st[0]:
            out |= 1 << i
        fb = 0
        for t in taps:
            fb ^= st[t]
        fb ^= st[1] & st[5] & st[9]
        st = st[1:] + [fb]
    return out


print("[*] Precomputing all 16-bit LFSR streams...", file=sys.stderr)
A_STREAMS = [lfsr_stream(s, [0, 1, 3, 5]) for s in range(1 << 16)]
C_STREAMS = [lfsr_stream(s, [0, 1, 2, 4]) for s in range(1 << 16)]
print("[*] Precompute done.", file=sys.stderr)


def recover_key_candidates(raw_bits):
    """Recover the two indistinguishable keys caused by l1/l2 symmetry."""
    target = sum((b & 1) << i for i, b in enumerate(raw_bits))
    ones = target

    # Output bit simplifies to: z & (x | y).
    # Therefore every target-1 position must have z=1.
    for c_seed, c_seq in enumerate(C_STREAMS):
        if (c_seq & ones) != ones:
            continue

        # Where z=1 and output=0, both l1 and l2 must output 0.
        forced_zero = c_seq & (~target & MASK)
        cand_a = []
        for seed, seq in enumerate(A_STREAMS):
            if (seq & forced_zero) == 0:
                cand_a.append((seed, seq & ones))

        # Need two l1/l2 streams whose OR covers all target-1 positions.
        for s1, cov1 in cand_a:
            missing = ones & ~cov1
            for s2, cov2 in cand_a:
                if (cov2 & missing) == missing:
                    k1 = (s1 << 32) | (s2 << 16) | c_seed
                    k2 = (s2 << 32) | (s1 << 16) | c_seed
                    return [k1] if k1 == k2 else [k1, k2]
    raise RuntimeError("No key candidate found")


def recv_until_prompt(sock):
    data = b""
    sock.settimeout(25)
    while b"> " not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode(errors="replace")


def decrypt_flag(raw_bits, text):
    salt = bytes.fromhex(re.search(r"Salt: ([0-9a-f]+)", text).group(1))
    iv = bytes.fromhex(re.search(r"IV: ([0-9a-f]+)", text).group(1))
    ct = bytes.fromhex(re.search(r"Ciphertext: ([0-9a-f]+)", text).group(1))

    # Important: server builds mix with bit 0 as the leftmost/MSB character.
    mix = int("".join(map(str, raw_bits)), 2).to_bytes(32, "big")
    aes_key = hashlib.sha1(salt + mix).digest()[:16]
    pt = aes_cbc_decrypt(aes_key, iv, ct)
    pad = pt[-1]
    return pt[:-pad].decode(errors="replace")


def one_attempt(force_swap=False):
    with socket.create_connection((HOST, PORT), timeout=25) as sock:
        banner = recv_until_prompt(sock)
        leaks = [1 if x == "Right" else 0 for x in re.findall(r"The cave says '(Left|Right)'", banner)]
        if len(leaks) != 256:
            raise RuntimeError(f"Expected 256 leaks, got {len(leaks)}")

        # Server leaks keystream[i] XOR ((i >> 3) & 1).
        raw_bits = [b ^ ((i >> 3) & 1) for i, b in enumerate(leaks)]
        keys = recover_key_candidates(raw_bits)

        # l1 and l2 are symmetric, so there are usually two indistinguishable keys.
        if len(keys) == 2:
            key = keys[1] if force_swap else keys[0]
        else:
            key = keys[0]

        print(f"[*] Trying key {key} / {key:#014x}", file=sys.stderr)
        sock.sendall(f"GUESS {key}\n".encode())

        out = b""
        sock.settimeout(10)
        try:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                out += chunk
        except socket.timeout:
            pass
        text = out.decode(errors="replace")
        print(text)

        if "Salt:" in text and "Ciphertext:" in text:
            flag = decrypt_flag(raw_bits, text)
            print("FLAG:", flag)
            return True
        return False


def main():
    # Because l1/l2 are identical and the combiner is symmetric, a single connection
    # cannot distinguish the first 16-bit block from the second. Reconnect until the
    # chosen ordering matches the server's actual random key; success probability ~1/2.
    attempt = 0
    while True:
        attempt += 1
        print(f"\n=== Attempt {attempt} ===", file=sys.stderr)
        try:
            # Alternate ordering; randomize if you prefer.
            if one_attempt(force_swap=(attempt % 2 == 0)):
                break
        except Exception as e:
            print(f"[!] Attempt failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
