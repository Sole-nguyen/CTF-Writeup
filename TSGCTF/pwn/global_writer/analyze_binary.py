#!/usr/bin/env python3
"""
Analyze the provided chal binary to get correct addresses
"""
import subprocess
import re

chal_path = '/mnt/c/Users/duynh/Documents/Code/CTF/TSGCTF/pwn/global_writer/chal'

print("[*] Analyzing chal binary...")

# Get symbols
result = subprocess.run(['readelf', '-s', chal_path], 
                       capture_output=True, text=True)

for line in result.stdout.split('\n'):
    if 'system' in line or 'puts' in line or 'values' in line or 'msg' in line:
        print(line)

print("\n[*] GOT entries...")
result = subprocess.run(['readelf', '-r', chal_path], 
                       capture_output=True, text=True)

for line in result.stdout.split('\n'):
    if 'system' in line or 'puts' in line or 'exit' in line:
        print(line)

print("\n[*] PLT entries...")
result = subprocess.run(['objdump', '-d', chal_path], 
                       capture_output=True, text=True)

for line in result.stdout.split('\n'):
    if 'system@plt>' in line or 'puts@plt>' in line:
        print(line)
