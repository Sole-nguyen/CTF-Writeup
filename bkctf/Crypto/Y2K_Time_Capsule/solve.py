#!/usr/bin/env python3
"""
Y2K Time Capsule - LCG Cracker
Given 5 consecutive LCG outputs, recover parameters and predict next 5.
  s[i+1] = a*s[i] + c (mod 1999)
  => a = (s[i+2]-s[i+1]) * modinv(s[i+1]-s[i], 1999) (mod 1999)
  => c = s[i+1] - a*s[i] (mod 1999)
"""
import socket
import re
import sys

MODULUS = 1999

def modinv(a, m):
    old_r, r = a % m, m
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_s % m

def crack_lcg(outputs):
    for i in range(len(outputs) - 2):
        d1 = (outputs[i+1] - outputs[i]) % MODULUS
        d2 = (outputs[i+2] - outputs[i+1]) % MODULUS
        if d1 == 0:
            continue
        a = (d2 * modinv(d1, MODULUS)) % MODULUS
        c = (outputs[i+1] - a * outputs[i]) % MODULUS
        # Verify
        state = outputs[0]
        valid = True
        for expected in outputs[1:]:
            state = (a * state + c) % MODULUS
            if state != expected:
                valid = False
                break
        if valid:
            return a, c
    raise ValueError("Could not crack LCG parameters from given outputs")

def predict_next(outputs, n=5):
    a, c = crack_lcg(outputs)
    state = outputs[-1]
    result = []
    for _ in range(n):
        state = (a * state + c) % MODULUS
        result.append(state)
    return result

def solve(host, port=1999, use_ssl=False):
    import ssl
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=host)

    data = b""
    while b"> " not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk

    print(data.decode())

    match = re.search(r'\[([0-9, ]+)\]', data.decode())
    if not match:
        print("Could not parse shown numbers!")
        s.close()
        return

    shown = [int(x.strip()) for x in match.group(1).split(',')]
    print(f"[*] Shown: {shown}")

    predictions = predict_next(shown)
    print(f"[*] Predicted: {predictions}")

    s.sendall((','.join(map(str, predictions)) + '\n').encode())

    response = s.recv(4096).decode()
    print(response)
    s.close()

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1999
    use_ssl = "--ssl" in sys.argv
    solve(host, port, use_ssl)
