#!/bin/bash
cd /mnt/c/Users/duynh/Documents/Code/CTF/TSGCTF/pwn/global_writer
cat PAYLOAD.txt | grep -E '^[0-9-]+$' | ./chal
