import multiprocessing
import time
from aes import AES

# Known parameters from output.txt
PT = bytes.fromhex("376f73334dc9db2a4d20734c0783ac69")
CT_EXPECTED = bytes.fromhex("9070f81f4de789663820e8924924732b")
KEY_PREFIX = bytes.fromhex("26ab77cadcca0ed41b03c8f2e5")
ENC_FLAG = bytes.fromhex("8e70387dc377a09cbc721debe27c468157b027e3e63fe02560506f70b3c72ca19130ae59c6eef47b734bb0147424ec936fc91dc658d15dee0b69a2dc24a78c44")

def brute_force_worker(start_val, end_val, result_queue):
    """Worker process to test a specific range of the 3-byte space."""
    for i in range(start_val, end_val):
        # Generate the 3 missing bytes
        suffix = i.to_bytes(3, byteorder='big')
        test_key = KEY_PREFIX + suffix
        
        try:
            # Test the key against our known PT/CT pair
            cipher = AES(test_key)
            if cipher.encrypt(PT) == CT_EXPECTED:
                result_queue.put(test_key)
                return
        except Exception:
            pass

def main():
    total_keys = 0xFFFFFF + 1
    num_cores = multiprocessing.cpu_count()
    chunk_size = total_keys // num_cores
    
    print(f"[*] Starting brute force across {num_cores} cores...")
    print(f"[*] Total keyspace: {total_keys}")
    
    start_time = time.time()
    
    processes = []
    result_queue = multiprocessing.Queue()
    
    for i in range(num_cores):
        start_val = i * chunk_size
        # Make sure the last core covers the remainder
        end_val = start_val + chunk_size if i < num_cores - 1 else total_keys 
        
        p = multiprocessing.Process(target=brute_force_worker, args=(start_val, end_val, result_queue))
        processes.append(p)
        p.start()

    # Wait for a successful key to be pushed to the queue
    found_key = result_queue.get()
    
    # Terminate remaining processes once the key is found
    for p in processes:
        p.terminate()

    print(f"\n[+] KEY FOUND: {found_key.hex()}")
    print(f"[*] Time taken: {time.time() - start_time:.2f} seconds")

    # Decrypt the flag
    print("\n[*] Decrypting flag...")
    cipher = AES(found_key)
    
    # The flag is 64 bytes (4 blocks of 16 bytes)
    decrypted_flag = b""
    for i in range(0, len(ENC_FLAG), 16):
        block = ENC_FLAG[i:i+16]
        decrypted_flag += cipher.decrypt(block)
        
    print(f"[+] Flag: {decrypted_flag.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    main()