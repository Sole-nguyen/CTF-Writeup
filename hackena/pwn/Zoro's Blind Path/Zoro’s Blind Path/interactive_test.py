#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

# Just interact to see what happens
r.interactive()
