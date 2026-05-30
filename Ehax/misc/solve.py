#!/usr/bin/env python3
"""Fire Maze CTF Solver - INFERNO SPRINT"""

import socket
import time
import heapq
from collections import deque

HOST = 'chall.ehax.in'
PORT = 31337

def precompute_fire(grid, rows, cols):
    """
    Dijkstra: compute earliest turn fire reaches each cell.
    Fire with speed K: takes K turns to spread 1 cell.
    Returns dict (r,c) -> earliest_fire_turn (default inf)
    """
    INF = float('inf')
    arrival = [[INF]*cols for _ in range(rows)]
    heap = []

    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch in '123':
                speed = int(ch)
                arrival[r][c] = 0
                heap.append((0, speed, r, c))

    while heap:
        t, spd, r, c = heapq.heappop(heap)
        if t > arrival[r][c]:
            continue
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                nt = t + spd
                if nt < arrival[nr][nc]:
                    arrival[nr][nc] = nt
                    # Inherit same speed (could also min with cell's own speed if it has fire)
                    ch2 = grid[nr][nc]
                    new_spd = min(spd, int(ch2)) if ch2 in '123' else spd
                    heapq.heappush(heap, (nt, new_spd, nr, nc))

    return arrival

def solve_round(grid, rows, cols, sr, sc):
    """
    BFS on state (r, c, turn).
    Returns move string or None.
    """
    fire = precompute_fire(grid, rows, cols)
    
    # Build portal map: letter -> list of (r,c)
    portal_map = {}
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if 'a' <= ch <= 'e':
                portal_map.setdefault(ch, []).append((r, c))

    # BFS
    # State: (r, c, turn)
    queue = deque()
    visited = set()
    
    # Safety check: make sure start isn't on fire at t=0
    if fire[sr][sc] <= 0:
        print(f"[!] Start position ({sr},{sc}) is on fire at t=0!")
        return None
    
    queue.append((sr, sc, 0, ""))
    visited.add((sr, sc, 0))
    
    dirs = [('W',-1,0),('S',1,0),('A',0,-1),('D',0,1)]
    
    while queue:
        r, c, t, path = queue.popleft()
        
        # Try regular moves
        for move, dr, dc in dirs:
            nr, nc = r+dr, c+dc
            nt = t + 1
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == '#':
                continue
            if fire[nr][nc] <= nt:  # fire arrives same time or earlier
                continue
            if (nr, nc, nt) in visited:
                continue
            visited.add((nr, nc, nt))
            new_path = path + move
            
            # Edge check
            if nr == 0 or nr == rows-1 or nc == 0 or nc == cols-1:
                return new_path
            
            # Portal use from new position
            ch = grid[nr][nc]
            if 'a' <= ch <= 'e':
                pts = portal_map.get(ch, [])
                for pr, pc in pts:
                    if (pr, pc) == (nr, nc):
                        continue
                    pt = nt + 1
                    if fire[pr][pc] <= pt:
                        continue
                    if (pr, pc, pt) in visited:
                        continue
                    visited.add((pr, pc, pt))
                    portal_path = new_path + 'P'
                    if pr == 0 or pr == rows-1 or pc == 0 or pc == cols-1:
                        return portal_path
                    queue.append((pr, pc, pt, portal_path))
            
            queue.append((nr, nc, nt, new_path))
    
    return None

def recv_all(s, timeout=5):
    s.settimeout(timeout)
    data = b''
    try:
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            data += chunk
    except:
        pass
    return data.decode('utf-8', errors='replace')

def parse_round(text, last_cols=None):
    """Parse round data from received text. Returns (rows,cols,sr,sc,limit,grid_lines)."""
    rows = cols = sr = sc = limit = None
    grid_lines = []
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('SIZE'):
            p = line.split()
            rows, cols = int(p[1]), int(p[2])
        elif line.startswith('START'):
            p = line.split()
            sr, sc = int(p[1]), int(p[2])
        elif line.startswith('LIMIT'):
            limit = int(line.split()[1])
        elif cols and len(line) == cols * 2 and all(c in '0123456789abcdef' for c in line):
            grid_lines.append(line)
    
    return rows, cols, sr, sc, limit, grid_lines

def main():
    print(f"[*] Connecting to {HOST}:{PORT}...")
    s = socket.socket()
    s.settimeout(15)
    s.connect((HOST, PORT))
    print("[+] Connected!")
    
    # Read initial banner + first round
    text = recv_all(s, timeout=5)
    print(text[:300])
    
    for round_num in range(1, 6):
        print(f"\n{'='*40}")
        print(f"=== PROCESSING ROUND {round_num}/5 ===")
        print(f"{'='*40}")
        
        # Parse round info
        rows, cols, sr, sc, limit, grid_lines = parse_round(text)
        
        if rows is None or not grid_lines:
            print("[!] Failed to parse round, reading more...")
            more = recv_all(s, timeout=5)
            text += more
            print(more[:500])
            rows, cols, sr, sc, limit, grid_lines = parse_round(text)
        
        if rows is None or len(grid_lines) < rows:
            print(f"[!] Parse error: rows={rows}, got {len(grid_lines)} grid lines")
            print("Text:", text[-500:])
            s.send(b'S\n')
            text = recv_all(s, timeout=5)
            continue
        
        # Decode grid
        grid = []
        for i, hex_row in enumerate(grid_lines[:rows]):
            try:
                row = bytes.fromhex(hex_row).decode('ascii')
                grid.append(list(row))
            except Exception as e:
                print(f"[!] Row {i} decode error: {e}")
                grid.append(['.'] * cols)
        
        print(f"[*] Grid {rows}x{cols}, Start ({sr},{sc}), Limit {limit}")
        print("[*] Sample grid rows:")
        for i in range(min(3, len(grid))):
            print(f"   Row {i}: {''.join(grid[i])}")
        
        # Solve
        t0 = time.time()
        path = solve_round(grid, rows, cols, sr, sc)
        t1 = time.time()
        
        if path is None:
            print("[!] No path found! Trying with relaxed fire constraint...")
            # Try ignoring fire (just find any path to edge)
            path = 'S' * (rows - 1 - sr) if rows - 1 - sr < cols - 1 - sc else 'D' * (cols - 1 - sc)
            if path == '':
                path = 'W'
        
        print(f"[+] Path: {path} ({len(path)} moves, solved in {t1-t0:.2f}s)")
        
        if len(path) > limit:
            print(f"[!] WARNING: path length {len(path)} exceeds limit {limit}!")
        
        # Send path
        s.send(path.encode() + b'\n')
        
        # Read response
        text = recv_all(s, timeout=8)
        print(f"[*] Response:\n{text[:600]}")
        
        if 'flag' in text.lower() or 'ehax{' in text.lower() or 'CTF{' in text:
            print("\n[!!!] FLAG FOUND:", text)
            import re
            flags = re.findall(r'[A-Za-z0-9_]+\{[^}]+\}', text)
            for f in flags:
                print("FLAG:", f)
            break
        
        if round_num == 5:
            print("[*] All 5 rounds done!")
            # Maybe flag comes after round 5
            time.sleep(1)
            final = recv_all(s, timeout=5)
            if final:
                print("Final response:", final)
                import re
                flags = re.findall(r'[A-Za-z0-9_]+\{[^}]+\}', final)
                for f in flags:
                    print("FLAG:", f)
    
    s.close()

if __name__ == '__main__':
    main()
