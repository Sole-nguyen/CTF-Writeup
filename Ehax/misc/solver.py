#!/usr/bin/env python3
"""
Fire Maze CTF Solver
Connects to the challenge, reads the maze, finds safe path to edge.
"""

import socket
import time
import re
from collections import deque

HOST = 'chall.ehax.in'
PORT = 31337

def recv_until(s, marker=None, timeout=5):
    """Receive data until marker is found or timeout."""
    s.settimeout(timeout)
    data = b''
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            if marker and marker in data:
                break
    except socket.timeout:
        pass
    return data

def strip_ansi(text):
    """Remove ANSI escape sequences."""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[mABCDEFGHJKLMPSTfhnrsu]|\x1b\[[?][0-9;]*[hl]|\x1b\[>[0-9;]*[mhl]|\x1b=[0-9;]*|\x1b\[|\x1b]|\x1b[=>]|\x1b[NOM]|\r')
    return ansi_escape.sub('', text)

def parse_maze(raw_text):
    """
    Parse the maze from raw text.
    Returns (grid, player_pos, fires, portals)
    grid: 2D list of chars
    player_pos: (row, col)
    fires: list of (row, col)
    portals: list of (row, col)
    """
    text = strip_ansi(raw_text)
    lines = text.split('\n')
    
    # Find maze boundaries - look for lines with # or | 
    maze_lines = []
    for line in lines:
        if any(c in line for c in ['#', '@', 'P', 'F', '*', '^', 'O', '.']):
            maze_lines.append(line)
    
    if not maze_lines:
        return None, None, [], []
    
    grid = []
    player_pos = None
    fires = []
    portals = []
    
    for r, line in enumerate(maze_lines):
        row = list(line)
        grid.append(row)
        for c, ch in enumerate(row):
            if ch in ['@', 'P', 'X']:  # player
                player_pos = (r, c)
            elif ch in ['F', 'f', '*', '^', '~']:  # fire
                fires.append((r, c))
            elif ch in ['O', 'o', 'V', 'v', 'T']:  # portal
                portals.append((r, c))
    
    return grid, player_pos, fires, portals

def find_path_bfs(grid, start, fires_set):
    """
    BFS to find path from start to any edge.
    Returns list of (row, col) positions, or None if no path.
    """
    if not grid or start is None:
        return None
    
    rows = len(grid)
    cols = max(len(row) for row in grid) if grid else 0
    
    # Check if start is already at edge
    r, c = start
    if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
        return [start]
    
    visited = {start}
    # Queue: (pos, path)
    queue = deque([(start, [start])])
    
    while queue:
        (r, c), path = queue.popleft()
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < len(grid[nr]) if nr < len(grid) else False:
                if (nr, nc) in visited:
                    continue
                cell = grid[nr][nc] if nc < len(grid[nr]) else ' '
                
                # Skip walls
                if cell in ['#', '|', '+', '-']:
                    continue
                # Skip fire
                if (nr, nc) in fires_set:
                    continue
                
                new_path = path + [(nr, nc)]
                
                # Check if at edge
                if nr == 0 or nr == rows - 1 or nc == 0 or nc == (len(grid[nr]) - 1):
                    return new_path
                
                visited.add((nr, nc))
                queue.append(((nr, nc), new_path))
    
    return None

def path_to_moves(path):
    """Convert path (list of positions) to move characters."""
    moves = []
    dirs = {
        (-1, 0): 'w',  # up
        (1, 0): 's',   # down
        (0, -1): 'a',  # left
        (0, 1): 'd',   # right
    }
    for i in range(1, len(path)):
        dr = path[i][0] - path[i-1][0]
        dc = path[i][1] - path[i-1][1]
        move = dirs.get((dr, dc), '?')
        moves.append(move)
    return moves

def debug_print(grid, player_pos, fires, portals):
    """Print the parsed maze for debugging."""
    print(f"Grid size: {len(grid)} x {max(len(r) for r in grid) if grid else 0}")
    print(f"Player: {player_pos}")
    print(f"Fires: {fires[:5]}{'...' if len(fires) > 5 else ''}")
    print(f"Portals: {portals}")
    print("Maze:")
    for i, row in enumerate(grid):
        print(f"{i:2}: {''.join(row)}")

def solve_maze_from_text(text):
    """Full maze solve pipeline."""
    grid, player_pos, fires, portals = parse_maze(text)
    
    if grid is None or player_pos is None:
        print("[!] Could not parse maze")
        print("Raw text:", repr(text[:500]))
        return None
    
    debug_print(grid, player_pos, fires, portals)
    
    fires_set = set(fires)
    path = find_path_bfs(grid, player_pos, fires_set)
    
    if path is None:
        print("[!] No path found!")
        # Try ignoring fires
        path = find_path_bfs(grid, player_pos, set())
        if path:
            print("[*] Found path ignoring fires")
    
    if path:
        moves = path_to_moves(path)
        print(f"[+] Path found: {len(moves)} moves: {' '.join(moves)}")
        return moves
    
    print("[!] No path found even ignoring fires!")
    return None


def main():
    print(f"[*] Connecting to {HOST}:{PORT}")
    
    while True:
        try:
            s = socket.socket()
            s.settimeout(15)
            s.connect((HOST, PORT))
            print("[+] Connected!")
            break
        except Exception as e:
            print(f"[-] Connection failed: {e}, retrying in 5s...")
            time.sleep(5)
    
    # Read initial data
    print("[*] Reading initial data...")
    data = recv_until(s, timeout=8)
    
    if not data:
        print("[!] No initial data received")
        # Try sending enter
        s.send(b'\n')
        data = recv_until(s, timeout=5)
    
    print(f"[*] Received {len(data)} bytes")
    print("Raw:", repr(data[:500]))
    
    text = data.decode('utf-8', errors='replace')
    print("Decoded:", text[:500])
    
    # Game loop
    round_num = 0
    while round_num < 5:
        print(f"\n[*] === Round {round_num + 1} ===")
        
        moves = solve_maze_from_text(text)
        
        if moves is None:
            print("[!] Could not solve, trying to read more...")
            more_data = recv_until(s, timeout=5)
            if more_data:
                text += more_data.decode('utf-8', errors='replace')
                moves = solve_maze_from_text(text)
        
        if moves:
            for move in moves:
                print(f"[*] Sending move: {move}")
                s.send(move.encode() + b'\n')
                time.sleep(0.1)
                
                # Read response
                resp = recv_until(s, timeout=3)
                if resp:
                    text = resp.decode('utf-8', errors='replace')
                    # Check for win/loss
                    if any(w in text.lower() for w in ['round', 'win', 'congratulation', 'flag', 'escaped', 'survived']):
                        print(f"[*] Status update: {text[:200]}")
                    if 'flag' in text.lower() or 'ehax{' in text.lower() or 'CTF{' in text:
                        print("[!!!] FLAG FOUND:", text)
                        break
                    if any(w in text.lower() for w in ['died', 'burned', 'game over', 'dead']):
                        print("[!] DIED:", text[:200])
                        break
        else:
            # No moves found, wait and read
            resp = recv_until(s, timeout=5)
            if resp:
                text = resp.decode('utf-8', errors='replace')
        
        round_num += 1
    
    s.close()

if __name__ == '__main__':
    main()
