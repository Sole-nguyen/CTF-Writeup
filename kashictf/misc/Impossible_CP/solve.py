#!/usr/bin/env python3
import argparse
import re
import socket
import subprocess
import sys
import time
from typing import Optional


FLAG_RE = re.compile(r"kashiCTF\{[^}]+\}")


class SocketIO:
    def __init__(self, host: str, port: int, timeout: float):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.file = self.sock.makefile("rwb", buffering=0)

    def readline(self) -> str:
        line = self.file.readline()
        if not line:
            raise EOFError("connection closed")
        return line.decode("utf-8", "ignore").rstrip("\n")

    def sendline(self, data: str) -> None:
        self.file.write((data + "\n").encode())

    def close(self) -> None:
        try:
            self.file.close()
        finally:
            self.sock.close()


class ProcessIO:
    def __init__(self, binary_path: str):
        self.proc = subprocess.Popen(
            [binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout

    def readline(self) -> str:
        line = self.stdout.readline()
        if line == "":
            raise EOFError("process closed stdout")
        return line.rstrip("\n")

    def sendline(self, data: str) -> None:
        self.stdin.write(data + "\n")
        self.stdin.flush()

    def close(self) -> None:
        try:
            self.stdin.close()
        except Exception:
            pass
        try:
            self.stdout.close()
        except Exception:
            pass
        self.proc.wait(timeout=1)

    def collect_stderr(self) -> str:
        try:
            return self.proc.stderr.read() if self.proc.stderr else ""
        except Exception:
            return ""


def read_int(io_obj) -> int:
    while True:
        line = io_obj.readline().strip()
        if not line:
            continue
        return int(line)


def solve_session(io_obj, verbose: bool = True) -> Optional[str]:
    t = read_int(io_obj)
    if verbose:
        print(f"[+] testcases = {t}", file=sys.stderr)

    for tc in range(1, t + 1):
        n = read_int(io_obj)
        ans = 0
        # Send all 32 bit-queries in one burst to avoid RTT bottlenecks.
        burst = "".join(f"? {n} {1 << bit}\n" for bit in range(32))
        io_obj.sendline = getattr(io_obj, "sendline")
        if isinstance(io_obj, ProcessIO):
            io_obj.stdin.write(burst)
            io_obj.stdin.flush()
        else:
            io_obj.file.write(burst.encode())
        for bit in range(32):
            b = read_int(io_obj)
            if b == 1:
                ans |= 1 << bit
        io_obj.sendline(f"! {ans}")
        if verbose:
            print(f"[+] case {tc}: A_n = {ans}", file=sys.stderr)

    # Read trailing output and search for flag.
    rest = []
    try:
        while True:
            rest.append(io_obj.readline())
    except Exception:
        pass
    text = "\n".join(rest)
    m = FLAG_RE.search(text)
    return m.group(0) if m else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="34.126.223.46")
    parser.add_argument("--port", type=int, default=17738)
    parser.add_argument("--timeout", type=float, default=4.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--retry-delay", type=float, default=1.0)
    parser.add_argument("--local", help="Path to local checker binary")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    verbose = not args.quiet

    if args.local:
        io_obj = ProcessIO(args.local)
        try:
            flag = solve_session(io_obj, verbose=verbose)
            if flag:
                print(flag)
                return 0
            stderr = io_obj.collect_stderr()
            m = FLAG_RE.search(stderr)
            if m:
                print(m.group(0))
                return 0
            if "Solved successfully" in stderr:
                if verbose:
                    print("[+] local checker solved (no /flag.txt in local env)", file=sys.stderr)
                return 0
            if verbose:
                print("[-] no flag found in local run output", file=sys.stderr)
            return 1
        finally:
            io_obj.close()

    last_err = None
    for attempt in range(1, args.retries + 1):
        try:
            io_obj = SocketIO(args.host, args.port, args.timeout)
            try:
                flag = solve_session(io_obj, verbose=verbose)
                if flag:
                    print(flag)
                    return 0
                if verbose:
                    print("[-] solved interaction but no flag string found", file=sys.stderr)
                return 1
            finally:
                io_obj.close()
        except Exception as exc:
            last_err = exc
            if verbose:
                print(f"[-] attempt {attempt}/{args.retries} failed: {exc}", file=sys.stderr)
            time.sleep(args.retry_delay)

    if verbose:
        print(f"[-] all retries failed: {last_err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
