#!/usr/bin/env python3
"""Entropy solver (ANSI dynamic maze) — Incognito CTF

Mục tiêu
- Kết nối tới service (nc HOST PORT)
- Parse raw ANSI stream thành từng frame (grid 51x51)
- Tìm cursor token '><' và goal token '▓▓'
- Xây open/closed map dựa trên background-color index (bg < 64 => wall)
- Chạy BFS theo *từng frame* để lấy bước đi tiếp theo, gửi WASD
- Scan raw bytes để bắt flag: IIITL{...}

Tại sao phải BFS theo từng frame?
- Màu nền (cage/pattern) thay đổi theo thời gian, nên path tĩnh dễ bị kẹt/reset.

Usage
  python3 solvve.py
  python3 solvve.py --host 34.131.216.230 --port 1340 --attempts 10 --verbose

Ghi chú
- Script này ưu tiên độ ổn định hơn là "spam" phím.
- Nếu bị timeout, script sẽ tự reconnect nhiều lần (attempts).

"""

from __future__ import annotations

import argparse
import collections
import re
import socket
import sys
import time
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Optional, Tuple


# ==== Challenge constants (reverse-engineered) ====
W = 51
H = 51
N_CELLS = W * H

# Frame starts with: ESC[2J ESC[H
CLS = b"\x1b[2J\x1b[H"

# Cell encoding (bytes): ESC[48;5;<bg>m [optional more SGR] <content> ESC[0m
# content is typically 2 visible chars (hex) but can be '><' or '▓▓' (UTF-8 multibyte)
CELL_RE = re.compile(
    rb"\x1b\[48;5;(\d+)m(?:\x1b\[[0-9;?]*m)*(.+?)\x1b\[0m"
)

FLAG_RE = re.compile(rb"IIITL\{[^}]+\}")

CURSOR_TOKEN = "><"
# Goal token observed
GOAL_TOKEN = "▓▓"

# Directions: (dy, dx, key)
DIRS = [(-1, 0, b"w"), (1, 0, b"s"), (0, -1, b"a"), (0, 1, b"d")]


@dataclass
class Frame:
    """A parsed frame: list of (bg_index, content_str) of length N_CELLS."""

    cells: List[Tuple[int, str]]

    def find_token(self, token: str) -> Optional[Tuple[int, int]]:
        """Return (y,x) of first cell whose content equals token."""
        for i, (_, ct) in enumerate(self.cells):
            if ct == token:
                return divmod(i, W)
        return None

    def find_goal(self) -> Optional[Tuple[int, int]]:
        """Goal token sometimes is '▓▓'. Be tolerant if decoding differs."""
        # Exact match first
        pos = self.find_token(GOAL_TOKEN)
        if pos is not None:
            return pos
        # Fallback: find any cell containing at least one '▓'
        for i, (_, ct) in enumerate(self.cells):
            if "▓" in ct:
                return divmod(i, W)
        return None


class AnsiMazeClient:
    """TCP client that can parse ANSI grid frames from a raw byte stream."""

    def __init__(self, host: str, port: int, sock_timeout: float = 0.2, verbose: bool = False):
        self.host = host
        self.port = port
        self.sock_timeout = sock_timeout
        self.verbose = verbose

        self.sock: Optional[socket.socket] = None
        self.buf = b""
        self.in_frame = False

    def connect(self) -> None:
        self.close()
        self.sock = socket.create_connection((self.host, self.port), timeout=5)
        self.sock.settimeout(self.sock_timeout)
        self.buf = b""
        self.in_frame = False

    def close(self) -> None:
        if self.sock is not None:
            try:
                self.sock.close()
            except Exception:
                pass
        self.sock = None

    def _recv_some(self) -> bytes:
        assert self.sock is not None
        try:
            return self.sock.recv(65536)
        except socket.timeout:
            return b""

    def send_key(self, key: bytes) -> None:
        """Send a single-byte key (w/a/s/d)."""
        assert self.sock is not None
        try:
            self.sock.sendall(key)
        except (BrokenPipeError, OSError):
            raise

    def read_until_frame_or_flag(self, deadline: float) -> Tuple[Optional[Frame], Optional[bytes]]:
        """Read from socket until we parse a full frame OR see a flag in raw buffer.

        Returns:
          (frame, flag_bytes)
          - if flag found: (None, flag)
          - if frame parsed: (Frame, None)
          - if deadline: (None, None)
        """

        while time.time() < deadline:
            chunk = self._recv_some()
            if chunk:
                self.buf += chunk
                m = FLAG_RE.search(self.buf)
                if m:
                    return (None, m.group(0))

            # Find frame start
            if not self.in_frame:
                idx = self.buf.find(CLS)
                if idx == -1:
                    continue
                # drop everything up to + including CLS
                self.buf = self.buf[idx + len(CLS) :]
                self.in_frame = True

            # Parse exactly N_CELLS cells.
            cells: List[Tuple[int, str]] = []
            endpos: Optional[int] = None
            for m in CELL_RE.finditer(self.buf):
                bg = int(m.group(1))
                # content may be UTF-8 blocks; ignore decode errors
                ct = m.group(2).decode("utf-8", "ignore")
                cells.append((bg, ct))
                if len(cells) == N_CELLS:
                    endpos = m.end()
                    break

            if endpos is None:
                continue

            # Consume bytes for this frame
            self.buf = self.buf[endpos:]
            self.in_frame = False
            return (Frame(cells=cells), None)

        return (None, None)


def bfs_next_step(openmask: List[bool], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """BFS on 4-neighborhood grid.

    openmask: length N_CELLS list of passable cells.
    Returns the *next* cell (y,x) to move into from start towards goal.
    """

    sy, sx = start
    gy, gx = goal
    sidx = sy * W + sx
    gidx = gy * W + gx

    q: Deque[int] = collections.deque([sidx])
    prev: Dict[int, Optional[int]] = {sidx: None}

    while q:
        idx = q.popleft()
        if idx == gidx:
            break
        y, x = divmod(idx, W)
        for dy, dx, _ in DIRS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W:
                nidx = ny * W + nx
                if nidx not in prev and openmask[nidx]:
                    prev[nidx] = idx
                    q.append(nidx)

    if gidx not in prev:
        return None

    # Backtrack from goal to find neighbor of start.
    cur = gidx
    while prev[cur] is not None and prev[cur] != sidx:
        cur = prev[cur]

    if prev[cur] is None:
        # start == goal
        return None

    ny, nx = divmod(cur, W)
    return (ny, nx)


def step_key(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> Optional[bytes]:
    """Return WASD byte for a single-step move."""
    y, x = from_pos
    ny, nx = to_pos
    dy, dx = ny - y, nx - x
    for ddy, ddx, key in DIRS:
        if (ddy, ddx) == (dy, dx):
            return key
    return None


def pick_stimulus_key(frame: Frame, cur: Tuple[int, int], threshold: int) -> bytes:
    """Pick a key likely to be a safe no-op but still triggers a redraw.

    Strategy:
      - Prefer a direction where the neighbor is currently "closed" (bg < threshold)
        so the move is rejected (no-op).
      - Otherwise default to 'a'.

    This is used when BFS can't find a path in the current frame, to advance time/state.
    """

    y, x = cur
    for dy, dx, key in DIRS:
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W:
            nb_bg = frame.cells[ny * W + nx][0]
            if nb_bg < threshold:
                return key
    return b"a"


def safe_to_send(cur: Tuple[int, int], key: bytes) -> bool:
    """Avoid sending moves that go out of bounds.

    In practice, border collisions sometimes correlate with weird resets.
    This guard is cheap and avoids obvious invalid moves.
    """

    y, x = cur
    if key == b"w" and y == 0:
        return False
    if key == b"s" and y == H - 1:
        return False
    if key == b"a" and x == 0:
        return False
    if key == b"d" and x == W - 1:
        return False
    return True


def solve_one(
    host: str,
    port: int,
    time_limit: float,
    threshold: int,
    retries_per_step: int,
    verbose: bool,
) -> Optional[str]:
    """Single connection attempt. Returns flag string if found, else None."""

    client = AnsiMazeClient(host, port, verbose=verbose)
    client.connect()
    deadline = time.time() + time_limit

    frame, flag = client.read_until_frame_or_flag(deadline)
    if flag:
        client.close()
        return flag.decode("ascii", "ignore")
    if frame is None:
        client.close()
        return None

    moves = 0

    while time.time() < deadline:
        # Always check for cursor position
        cur = frame.find_token(CURSOR_TOKEN)
        if cur is None:
            # Frame malformed; just read again
            frame, flag = client.read_until_frame_or_flag(deadline)
            if flag:
                client.close()
                return flag.decode("ascii", "ignore")
            if frame is None:
                break
            continue

        goal = frame.find_goal() or (49, 49)  # fallback to known location

        # Build dynamic passability map from background index.
        openmask = [(bg >= threshold) for (bg, _) in frame.cells]
        openmask[cur[0] * W + cur[1]] = True
        openmask[goal[0] * W + goal[1]] = True

        nxt = bfs_next_step(openmask, cur, goal)

        # Decide what to send, then consume exactly ONE frame per send.
        if nxt is None:
            # No path in current frame -> stimulate next frame
            key = pick_stimulus_key(frame, cur, threshold)
            if safe_to_send(cur, key):
                client.send_key(key)
                moves += 1

            frame, flag = client.read_until_frame_or_flag(deadline)
            if flag:
                client.close()
                return flag.decode("ascii", "ignore")
            if frame is None:
                break
            continue

        key = step_key(cur, nxt)
        if key is None or not safe_to_send(cur, key):
            # Shouldn't happen; fall back to stimulus
            key = pick_stimulus_key(frame, cur, threshold)

        # Try the planned step; if it doesn't move, retry a few times.
        for _ in range(retries_per_step):
            if safe_to_send(cur, key):
                client.send_key(key)
                moves += 1

            frame2, flag = client.read_until_frame_or_flag(deadline)
            if flag:
                client.close()
                return flag.decode("ascii", "ignore")
            if frame2 is None:
                client.close()
                return None

            cur2 = frame2.find_token(CURSOR_TOKEN)
            frame = frame2
            if cur2 is not None and cur2 != cur:
                break

        if verbose and moves % 120 == 0:
            cur_now = frame.find_token(CURSOR_TOKEN)
            print(f"[dbg] moves={moves} cur={cur_now} goal={goal} last_key={key.decode()}")

    client.close()
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Entropy ANSI maze solver (BFS-per-frame)")
    ap.add_argument("--host", default="34.131.216.230")
    ap.add_argument("--port", type=int, default=1340)
    ap.add_argument("--attempts", type=int, default=10, help="Number of reconnect attempts")
    ap.add_argument("--time-limit", type=float, default=58.0, help="Seconds per attempt")
    ap.add_argument("--threshold", type=int, default=64, help="bg<threshold treated as wall")
    ap.add_argument("--retries", type=int, default=6, help="Retries for a planned step")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    for attempt in range(1, args.attempts + 1):
        if args.verbose:
            print(f"[*] attempt {attempt}/{args.attempts} connect {args.host}:{args.port}")
        try:
            flag = solve_one(
                host=args.host,
                port=args.port,
                time_limit=args.time_limit,
                threshold=args.threshold,
                retries_per_step=args.retries,
                verbose=args.verbose,
            )
        except (ConnectionError, OSError, socket.error):
            flag = None

        if flag:
            print(flag)
            return 0

    print("[!] no flag (increase --attempts or tweak --threshold/--retries)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
