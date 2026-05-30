#!/usr/bin/env python3
import socket
import hashlib
import string
from functools import lru_cache

@lru_cache(maxsize=100000)
def _quantum_field_multiply(val_x, val_y, bit_width=512):
    assert val_x.bit_length() <= bit_width and val_y.bit_length() <= bit_width
    if val_x == 0 or val_y == 0:
        return 0
    if val_x == 1:
        return val_y
    if val_y == 1:
        return val_x
    bit_width >>= 1
    high_x, low_x = val_x >> bit_width, val_x & (1 << bit_width) - 1
    high_y, low_y = val_y >> bit_width, val_y & (1 << bit_width) - 1
    low_product = _quantum_field_multiply(low_x, low_y, bit_width)
    high_product = _quantum_field_multiply(high_x, high_y, bit_width)
    cross_sum = _quantum_field_multiply(
        high_x ^ low_x, high_y ^ low_y, bit_width) ^ low_product
    fermat_term = _quantum_field_multiply(
        1 << (bit_width - 1), high_product, bit_width) ^ low_product
    return cross_sum << bit_width | fermat_term

class QuantumNimber:
    def __init__(self, essence):
        self.essence = essence

    def __add__(self, other):
        return QuantumNimber(self.essence ^ other.essence)

    def __sub__(self, other):
        return QuantumNimber(self.essence ^ other.essence)

    def __mul__(self, other):
        return QuantumNimber(_quantum_field_multiply(self.essence, other.essence))

    def __pow__(self, exponent):
        assert exponent >= 0
        base = self
        result = QuantumNimber(1)
        while exponent > 0:
            if exponent % 2 == 1:
                result = result * base
            base *= base
            exponent //= 2
        return result

    def __repr__(self):
        return str(self.essence)

def solve_pow(prefix, difficulty):
    """Brute force PoW solution"""
    for i in range(100000000):
        solution = str(i)
        combined = prefix + solution
        hash_result = hashlib.sha256(combined.encode()).hexdigest()
        if hash_result.startswith('0' * difficulty):
            return solution
    return None

def solve_dragon_meetinthemiddle(magic_power_value, dragon_life_value):
    """
    Meet-in-the-middle attack:
    Compute all 2-combinations and store in a hash table
    Then search for matching 2-combinations
    """
    magic_power = QuantumNimber(magic_power_value)
    target = dragon_life_value
    
    print(f"[*] Pre-computing powers...")
    
    # Pre-compute powers up to a larger limit
    max_exp = 100
    powers = {}
    for i in range(max_exp):
        powers[i] = (magic_power ** i).essence
        if i < 10:
            print(f"    magic_power^{i} = {powers[i]}")
    
    print(f"[*] Building hash table for 2-combinations...")
    # Build hash table for all 2-combinations (including using same power twice)
    two_combos = {}
    for i in range(max_exp):
        for j in range(i, max_exp):
            val = powers[i] ^ powers[j]
            if val not in two_combos:
                two_combos[val] = []
            two_combos[val].append((i, j))
    
    print(f"[*] Created {len(two_combos)} unique 2-combinations")
    
    print(f"[*] Searching with meet-in-the-middle...")
    
    # Search for 4-combinations by matching two 2-combinations
    for val1, combos1 in two_combos.items():
        target_val = target ^ val1
        if target_val in two_combos:
            # Found a match!
            combo1 = combos1[0]
            combo2 = two_combos[target_val][0]
            result = [combo1[0], combo1[1], combo2[0], combo2[1]]
            print(f"[*] Found 4-spell solution: {result}")
            return result
    
    # Try 3-combinations more exhaustively
    print(f"[*] Trying 3-combinations...")
    for i in range(max_exp):
        if i % 10 == 0:
            print(f"    Checking exponent {i}/{max_exp}...")
        for val2, combos2 in two_combos.items():
            test_val = target ^ powers[i] ^ val2
            if test_val == 0:
                combo2 = combos2[0]
                result = [i, combo2[0], combo2[1]]
                print(f"[*] Found 3-spell solution: {result}")
                return result
    
    # Try 2-combinations directly
    print(f"[*] Trying direct 2-combinations...")
    if target in two_combos:
        combo = two_combos[target][0]
        result = [combo[0], combo[1]]
        print(f"[*] Found 2-spell solution: {result}")
        return result
    
    # Try 1-combination
    print(f"[*] Trying single spell...")
    for i in range(max_exp):
        if powers[i] == target:
            return [i]
    
    return None

# Connect to server
HOST = '61.14.233.78'
PORT = 6669

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Read banner and PoW challenge
data = b''
s.settimeout(2)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b'Your proof:' in data:
            break
except socket.timeout:
    pass
s.settimeout(None)

data = data.decode()
print(data)

# Parse challenge
prefix = None
lines = data.split('\n')
for line in lines:
    if 'Challenge:' in line:
        prefix = line.split('Challenge:')[1].strip()
        print(f"[*] PoW prefix: {prefix}")
        break

if not prefix:
    print("[!] Could not parse PoW challenge")
    s.close()
    exit(1)

# Solve PoW
print("[*] Solving PoW...")
pow_solution = solve_pow(prefix, 4)
print(f"[*] PoW solution: {pow_solution}")

# Send PoW solution
s.sendall((pow_solution + '\n').encode())

# Read response including magic power
print("[*] Reading response after PoW...")
data = b''
s.settimeout(5)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b'Spell Intensity>' in data or len(data) > 8192:
            break
except socket.timeout:
    pass
s.settimeout(None)

data = data.decode()
print(data)

# Parse magic power and dragon life
magic_power_value = None
dragon_life_value = None

lines = data.split('\n')
for line in lines:
    if 'Magic Power:' in line:
        magic_power_value = int(line.split(':')[1].strip())
        print(f"[*] Magic Power: {magic_power_value}")
    if "Dragon's Life Force:" in line:
        dragon_life_value = int(line.split(':')[1].strip())
        print(f"[*] Dragon Life: {dragon_life_value}")

if not magic_power_value or not dragon_life_value:
    print("[!] Could not parse magic power or dragon life")
    s.close()
    exit(1)

# Solve for spell intensities
print("[*] Solving for spell intensities...")
spells = solve_dragon_meetinthemiddle(magic_power_value, dragon_life_value)

if spells:
    print(f"[*] Found solution: {spells}")
    # Pad with 0s if needed
    while len(spells) < 4:
        spells.append(0)
    
    # Cast spells
    for i, spell in enumerate(spells[:4]):
        print(f"[*] Casting spell {i+1}: intensity {spell}")
        s.sendall((str(spell) + '\n').encode())
        try:
            data = s.recv(4096).decode()
            print(data)
        except:
            pass
else:
    print("[!] Could not find solution")
    s.close()
    exit(1)

# Read final response (should have the flag)
print("[*] Reading final response...")
try:
    s.settimeout(3)
    while True:
        try:
            data = s.recv(4096).decode()
            if data:
                print(data)
            else:
                break
        except:
            break
except:
    pass

s.close()
