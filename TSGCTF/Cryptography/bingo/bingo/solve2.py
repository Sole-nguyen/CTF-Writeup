from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
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
    
    print(f"N bit length: {N.bit_length()}")
    print(f"hash_p bit length: {hash_p.bit_length()}")
    print(f"e = {e}")
    
    base_msg = b"Get Flag."
    
    # Optimized approach: Generate larger lookup table of sig -> hash
    # Since we need sig^e mod N == hash, and hash < hash_p
    # We compute hashes for small signatures and store them
    
    print("Building hash lookup table from signatures...")
    sig_to_hash = {}
    MAX_SIG = 1000000  # Try up to 1 million
    
    for sig in range(2, MAX_SIG):
        h = pow(sig, e, N)
        # Only store if hash is in valid range (less than hash_p)
        if h < hash_p:
            sig_to_hash[h] = sig
        
        if sig % 100000 == 0:
            print(f"  Processed {sig}/{MAX_SIG} signatures, table size: {len(sig_to_hash)}")
    
    print(f"Built lookup table with {len(sig_to_hash)} entries")
    
    # Now search for a message whose hash matches one in our table
    print("Searching for a matching message...")
    
    for attempt in range(10000000):  # Try up to 10 million messages
        # Generate random suffix
        suffix_int = random.randint(0, 2**128)  # Use larger random space
        suffix = long_to_bytes(suffix_int)
        msg = base_msg + suffix
        
        h = cvhp_hash(msg, hash_p, alpha, beta)
        
        if h in sig_to_hash:
            sig = sig_to_hash[h]
            print(f"\n[!!!] BINGO! Found match after {attempt+1} attempts!")
            print(f"Message (hex): {msg.hex()}")
            print(f"Hash: {h}")
            print(f"Signature: {sig}")
            print(f"Verification: {pow(sig, e, N)} == {h}? {pow(sig, e, N) == h}")
            
            # Send to server
            io.sendlineafter(b'input message (hex): ', msg.hex().encode())
            io.sendlineafter(b'input signature (int): ', str(sig).encode())
            
            # Get result
            result = io.recvall(timeout=3).decode()
            print("\nServer response:")
            print(result)
            
            io.close()
            return
        
        if (attempt + 1) % 10000 == 0:
            print(f"  Tried {attempt+1} messages...")
    
    print("No match found :(")
    io.close()

if __name__ == "__main__":
    solve()
