#!/usr/bin/env python3
from pwn import *
import time
import re

context.log_level = 'info'

log.info("Connecting to Marauder Matchup challenge...")
conn = remote('marauder.ctf.ritsec.club', 1112)

conn.recvuntil(b'interpreting\n', timeout=5)
log.info("Received 'interpreting' prompt")

log.info("The server is likely running the arsenal binary")
log.info("Based on the binary analysis, it uses getpid() and kill()")
log.info("The challenge asks us to find and kill an enemy process")

log.info("Trying to interact with the server...")
conn.sendline(b'help')
time.sleep(1)

try:
    data = conn.recvall(timeout=5)
    if data:
        log.success(f"Received: {data.decode('utf-8', errors='ignore')}")
        if b'RITSEC{' in data:
            match = re.search(b'RITSEC\{[^}]+\}', data)
            if match:
                log.success(f"FLAG: {match.group(0).decode()}")
except:
    log.error("No response from server")

conn.close()

log.info("")
log.info("Note: The arsenal binary is ARM64 architecture")
log.info("It needs to be reversed using ARM64 tools or emulated with qemu-aarch64")
log.info("The flag is likely revealed when the correct PID is killed")
