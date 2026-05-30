#!/usr/bin/env python3
import socket
import hashlib
import string
from functools import lru_cache

@lru_cache
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
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    for i in range(100000000):
        solution = str(i)
        combined = prefix + solution
        hash_result = hashlib.sha256(combined.encode()).hexdigest()
        if hash_result.startswith('0' * difficulty):
            return solution
    return None

def solve_dragon(magic_power_value, dragon_life_value):
    """
    We need to find spell intensities such that:
    dragon_life - (magic_power^i1) - (magic_power^i2) - ... = 0
    
    In nimber arithmetic, subtraction is XOR, so:
    dragon_life XOR (magic_power^i1) XOR (magic_power^i2) XOR ... = 0
    """
    magic_power = QuantumNimber(magic_power_value)
    target = dragon_life_value
    
    # We have 4 spell casts. Let's try to find a combination
    # Strategy: We can express the target as a linear combination in nimber field
    
    # Let's try simple exponents first
    spells = []
    current = target
    
    # Try powers from 0 to small numbers
    for exp in range(10):
        if current == 0:
            break
        damage = (magic_power ** exp).essence
        if damage != 0:
            current ^= damage
            spells.append(exp)
            if current == 0:
                break
    
    if current == 0:
        return spells
    
    # If simple approach doesn't work, try brute force small combinations
    from itertools import combinations_with_replacement
    
    for combo_size in range(1, 5):
        for combo in combinations_with_replacement(range(20), combo_size):
            test_val = target
            for exp in combo:
                damage = (magic_power ** exp).essence
                test_val ^= damage
            if test_val == 0:
                return list(combo)
    
    return None

# Connect to server
HOST = '61.14.233.78'
PORT = 6669

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Read banner and PoW challenge - may need multiple receives
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

# Parse challenge - look for the format "Challenge: xxxx"
prefix = None
lines = data.split('\n')
for line in lines:
    if 'Challenge:' in line:
        prefix = line.split('Challenge:')[1].strip()
        print(f"[*] PoW prefix: {prefix}")
        break

if not prefix:
    print("[!] Could not parse PoW challenge")
    print("[DEBUG] Full data received:")
    print(repr(data))
    s.close()
    exit(1)

# Solve PoW
print("[*] Solving PoW...")
pow_solution = solve_pow(prefix, 4)
print(f"[*] PoW solution: {pow_solution}")

# Send PoW solution
s.sendall((pow_solution + '\n').encode())

# Read response including magic power
data = b''
s.settimeout(2)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b'Spell Intensity>' in data:
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
spells = solve_dragon(magic_power_value, dragon_life_value)

if spells:
    print(f"[*] Found solution: {spells}")
    # Pad with 0s if needed
    while len(spells) < 4:
        spells.append(0)
    
    # Cast spells
    for i, spell in enumerate(spells[:4]):
        s.sendall((str(spell) + '\n').encode())
        data = s.recv(4096).decode()
        print(data)
else:
    print("[!] Could not find solution")

# Read final response
try:
    data = s.recv(4096).decode()
    print(data)
except:
    pass

s.close()
