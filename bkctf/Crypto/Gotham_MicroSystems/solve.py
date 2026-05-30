import socket
import ssl
import re
import time

HOST = "gotham-microsystems-1a47a39a21746b58.instancer.batmans.kitchen"
PORT = 1337
USE_SSL = True
BLOCK_SIZE = 16


def create_connection():
    s = socket.create_connection((HOST, PORT), timeout=60)
    if USE_SSL:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=HOST)
    s.settimeout(60)
    return s


def recv_until(s, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def connect_and_get_ct():
    s = create_connection()
    welcome = recv_until(s, b">")
    text = welcome.decode("utf-8", errors="replace")
    m = re.search(r"\(([0-9A-Fa-f]+)\)", text)
    if not m:
        raise ValueError(f"Could not find ciphertext in:\n{text}")
    return bytes.fromhex(m.group(1)), s


def oracle(s, ct_bytes: bytes) -> str:
    s.sendall(ct_bytes.hex().upper().encode() + b"\n")
    data = b""
    while True:
        try:
            chunk = s.recv(4096)
        except Exception:
            return "error"
        if not chunk:
            return "error"
        data += chunk
        if b"Successful" in data:
            return "success"
        if b"Exiting" in data or b"Unknown Exception" in data:
            return "error"
        if (b"Bad Padding" in data or b"Invalid API Key" in data) and b">" in data:
            return "bad_padding" if b"Bad Padding" in data else "valid"


def fresh_connection(max_retries=10):
    for attempt in range(max_retries):
        s = None
        try:
            s = create_connection()
            recv_until(s, b">")
            return s
        except Exception as e:
            print(f"  [reconnect attempt {attempt+1}/{max_retries} failed: {e}]", flush=True)
            try:
                s.close()
            except Exception:
                pass
            time.sleep(3)
    raise Exception(f"Could not connect after {max_retries} attempts")


def oracle_with_retry(s_ref: list, ct_bytes: bytes) -> str:
    for attempt in range(5):
        result = oracle(s_ref[0], ct_bytes)
        if result != "error":
            return result
        print(f"  [oracle error, reconnecting attempt {attempt+1}]", flush=True)
        try:
            s_ref[0].close()
        except Exception:
            pass
        s_ref[0] = fresh_connection()
    return "error"


def decrypt_block(ciphertext: bytes, block_idx: int) -> bytes:
    C_prev = ciphertext[(block_idx - 1) * BLOCK_SIZE: block_idx * BLOCK_SIZE]
    C_curr = ciphertext[block_idx * BLOCK_SIZE: (block_idx + 1) * BLOCK_SIZE]
    intermediate = bytearray(BLOCK_SIZE)

    s_ref = [fresh_connection()]

    for byte_pos in range(BLOCK_SIZE - 1, -1, -1):
        pad_val = BLOCK_SIZE - byte_pos
        forged = bytearray(BLOCK_SIZE)
        for k in range(byte_pos + 1, BLOCK_SIZE):
            forged[k] = intermediate[k] ^ pad_val

        found = False
        for guess in range(256):
            forged[byte_pos] = guess
            test_ct = bytes(forged) + C_curr

            result = oracle_with_retry(s_ref, test_ct)

            if result == "valid":
                # Anti-false-positive: verify last byte isn't e.g. \x02\x02
                if byte_pos == BLOCK_SIZE - 1:
                    forged2 = bytearray(forged)
                    forged2[byte_pos - 1] ^= 1
                    r2 = oracle_with_retry(s_ref, bytes(forged2) + C_curr)
                    if r2 != "valid":
                        continue

                intermediate[byte_pos] = guess ^ pad_val
                plain_byte = intermediate[byte_pos] ^ C_prev[byte_pos]
                print(f"  [{block_idx}][{byte_pos:2d}] = 0x{plain_byte:02x}  ({chr(plain_byte) if 32 <= plain_byte < 127 else '.'})",
                      flush=True)
                found = True
                break

        if not found:
            print(f"  WARNING: could not find byte {byte_pos} in block {block_idx}")

    s_ref[0].close()
    return bytes(intermediate[i] ^ C_prev[i] for i in range(BLOCK_SIZE))


def main():
    print("Connecting to get ciphertext...")
    ct, init_conn = connect_and_get_ct()
    init_conn.close()
    print(f"Ciphertext ({len(ct)} bytes): {ct.hex()}")

    num_blocks = len(ct) // BLOCK_SIZE
    print(f"Blocks: {num_blocks}  (block 0 = encrypted salt, blocks 1+ = flag)\n")

    plaintext = b""
    for i in range(3, num_blocks):
        print(f"Decrypting block {i} ...")
        block = decrypt_block(ct, i)
        plaintext += block
        print(f"  => {block}\n")

    pad = plaintext[-1]
    if 1 <= pad <= BLOCK_SIZE:
        plaintext = plaintext[:-pad]

    print("=" * 50)
    print(f"FLAG: {plaintext.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    main()
