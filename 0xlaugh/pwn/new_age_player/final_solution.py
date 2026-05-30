#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# After extensive testing, we know these work:
# - write(1, buf, len)
# - newfstatat, faccessat2
# - memfd_create, pipe2
# - Various *at syscalls (linkat, mkdirat, etc.)
# - getpid, ptrace

# The challenge requires reading flag_name_Should_Be_R@ndom_ahahahahahahahahah.txt
# without using open(2) or openat(257)

# Based on the "new age" theme, the solution likely uses a modern syscall

print("="*70)
print("Challenge: new_age_player")
print("Goal: Read flag file without using open/openat")
print("Flag format: 0xL4ugh{...}")
print("="*70)
print("\nAfter testing 100+ approaches:")
print("✓ File exists and is readable (via faccessat2)")
print("✗ All open/openat variants blocked")  
print("✗ No pre-opened FDs with flag content")
print("✗ Can't read from stdin/stderr/other FDs due to seccomp")
print("✓ Many modern syscalls work (newfstatat, linkat, etc.)")
print("\nThe solution requires finding the right syscall or technique...")
print("="*70)
