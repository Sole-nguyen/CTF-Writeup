#!/usr/bin/env python3
import socket
import time
import sys
import select

host = '14.225.212.104'
port = 9999

print(f'Connecting to {host}:{port}...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((host, port))
    print('Connected!')
    s.setblocking(False)
except Exception as e:
    print(f'Connection failed: {e}')
    sys.exit(1)

def recv_until_quiet(sock, timeout=2):
    data = b''
    start = time.time()
    while time.time() - start < timeout:
        ready = select.select([sock], [], [], 0.1)
        if ready[0]:
            try:
                chunk = sock.recv(4096)
                if chunk:
                    data += chunk
                    start = time.time()  # Reset timeout on new data
            except BlockingIOError:
                pass
        time.sleep(0.1)
    return data.decode('utf-8', errors='ignore')

# Get welcome message
print("Waiting for welcome message...")
welcome = recv_until_quiet(s, timeout=3)
print(welcome)

# Strategy: Use gun (option 1) to kill monster silently
# Monster likely has 10 HP (we have 10 bullets)
for i in range(1, 11):
    print(f"\n--- Shot {i} ---")
    s.send(b'1\n')
    time.sleep(0.5)
    response = recv_until_quiet(s, timeout=2)
    print(response)
    if 'Congrats' in response or 'flag' in response.lower() or 'VSL' in response:
        print("\n=== FLAG FOUND ===")
        break
    if 'Out of bullet' in response or 'goodbye' in response.lower():
        print("Game over!")
        break

s.close()
