from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
import itertools
import random

def cvhp_hash(message_bytes, hash_p, alpha, beta):
    m = bytes_to_long(message_bytes)
    m_1 = m % (hash_p - 1)
    m_2 = m // (hash_p - 1)
    val1 = pow(alpha, m_1, hash_p)
    val2 = pow(beta, m_2, hash_p)
    h = (val1 * val2) % hash_p
    return h

def solve():
    # Connect to server
    io = remote('35.194.98.181', 10961)
    # io = process(['python', 'server.py'])
    
    # Get public parameters
    io.recvuntil(b'N = ')
    N = int(io.recvline().strip())
    io.recvuntil(b'e = ')
    e = int(io.recvline().strip())
    io.recvuntil(b'hash_p = ')
    hash_p = int(io.recvline().strip())
    io.recvuntil(b'alpha = ')
    alpha = int(io.recvline().strip())
    io.recvuntil(b'beta = ')
    beta = int(io.recvline().strip())
    
    print(f"N = {N}")
    print(f"e = {e}")
    print(f"hash_p = {hash_p}")
    print(f"alpha = {alpha}")
    print(f"beta = {beta}")
    print(f"N bit length: {N.bit_length()}")
    print(f"hash_p bit length: {hash_p.bit_length()}")
    
    # Key insight: The hash H is computed mod hash_p (1024 bits)
    # But signature verification is mod N (1024 bits, p*q where p,q are 512 bits)
    # 
    # The attack: Try messages and hope the hash H happens to be
    # a perfect e-th power modulo N. This is the "bingo" moment.
    # 
    # With e = 65537, the probability is roughly 1/e for random values
    # So we need to try many different messages
    
    base_msg = b"Get Flag."
    
    # Strategy: Try random suffixes and check if hash is a perfect e-th power mod N
    # by computing small candidate signatures and checking
    
    # Better strategy: Generate candidate signatures s, compute h = s^e mod N,
    # then try to find a message that hashes to h
    
    # Actually, let's just try many random messages and for each,
    # try small signature values to see if sig^e mod N == hash
    
    print("Trying different messages...")
    attempts = 0
    
    # Try messages with different suffixes
    for i in range(10000):
        # Generate random suffix
        suffix = long_to_bytes(random.randint(0, 2**32))
        msg = base_msg + suffix
        h = cvhp_hash(msg, hash_p, alpha, beta)
        
        attempts += 1
        if attempts % 100 == 0:
            print(f"Attempts: {attempts}, current hash: {h}")
        
        # Try small signatures
        for sig in range(2, 10000):
            if pow(sig, e, N) == h:
                print(f"\n[!] BINGO! Found valid signature!")
                print(f"Message: {msg.hex()}")
                print(f"Hash: {h}")
                print(f"Signature: {sig}")
                
                io.sendlineafter(b'input message (hex): ', msg.hex().encode())
                io.sendlineafter(b'input signature (int): ', str(sig).encode())
                result = io.recvall(timeout=2).decode()
                print(result)
                io.close()
                return
    
    print("No luck, trying alternate approach...")
    
    # Try the inverse: pick small signatures and see if we can find a matching message
    print("Generating hash table from small signatures...")
    sig_to_hash = {}
    for sig in range(2, 100000):
        h = pow(sig, e, N)
        if h < hash_p:  # Only valid if h is in range
            sig_to_hash[h] = sig
        if sig % 10000 == 0:
            print(f"Generated {sig} signatures...")
    
    print(f"Generated {len(sig_to_hash)} candidate hashes")
    
    # Now try to find a message that produces one of these hashes
    print("Searching for matching message...")
    for i in range(1000000):
        suffix = long_to_bytes(random.randint(0, 2**64))
        msg = base_msg + suffix
        h = cvhp_hash(msg, hash_p, alpha, beta)
        
        if h in sig_to_hash:
            sig = sig_to_hash[h]
            print(f"\n[!] BINGO! Found matching message!")
            print(f"Message: {msg.hex()}")
            print(f"Hash: {h}")
            print(f"Signature: {sig}")
            
            io.sendlineafter(b'input message (hex): ', msg.hex().encode())
            io.sendlineafter(b'input signature (int): ', str(sig).encode())
            result = io.recvall(timeout=2).decode()
            print(result)
            io.close()
            return
        
        if i % 10000 == 0:
            print(f"Tried {i} messages...")
    
    io.close()

if __name__ == "__main__":
    solve()
