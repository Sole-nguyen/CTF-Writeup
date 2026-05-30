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

def solve_dragon_smart(magic_power_value, dragon_life_value):
    """
    Smart approach: In nimber arithmetic over GF(2^512), we have:
    - Addition/Subtraction is XOR
    - Multiplication follows special rules
    
    We need: dragon_life XOR (magic_power^i1) XOR (magic_power^i2) XOR (magic_power^i3) XOR (magic_power^i4) = 0
    
    Key insight: We can use powers of 2 as exponents
    magic_power^0 = 1
    magic_power^1 = magic_power
    magic_power^2, magic_power^3, etc.
    
    Strategy: Try to represent dragon_life as sum (XOR) of powers of magic_power
    """
    magic_power = QuantumNimber(magic_power_value)
    target = dragon_life_value
    
    print(f"[*] Computing useful powers...")
    
    # Pre-compute some powers
    powers = {}
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        powers[i] = (magic_power ** i).essence
        print(f"    magic_power^{i} = {powers[i]}")
    
    # Try combinations of 4 or fewer powers
    from itertools import combinations_with_replacement
    
    print(f"[*] Searching for combination...")
    
    # Try using 1 spell
    for exp in range(20):
        if exp not in powers:
            powers[exp] = (magic_power ** exp).essence
        if powers[exp] == target:
            return [exp]
    
    # Try using 2 spells
    for exp1 in range(15):
        if exp1 not in powers:
            powers[exp1] = (magic_power ** exp1).essence
        for exp2 in range(15):
            if exp2 not in powers:
                powers[exp2] = (magic_power ** exp2).essence
            if powers[exp1] ^ powers[exp2] == target:
                return [exp1, exp2]
    
    # Try using 3 spells
    for exp1 in range(12):
        if exp1 not in powers:
            powers[exp1] = (magic_power ** exp1).essence
        for exp2 in range(12):
            if exp2 not in powers:
                powers[exp2] = (magic_power ** exp2).essence
            for exp3 in range(12):
                if exp3 not in powers:
                    powers[exp3] = (magic_power ** exp3).essence
                if powers[exp1] ^ powers[exp2] ^ powers[exp3] == target:
                    return [exp1, exp2, exp3]
    
    # Try using 4 spells
    for exp1 in range(10):
        if exp1 not in powers:
            powers[exp1] = (magic_power ** exp1).essence
        for exp2 in range(10):
            if exp2 not in powers:
                powers[exp2] = (magic_power ** exp2).essence
            for exp3 in range(10):
                if exp3 not in powers:
                    powers[exp3] = (magic_power ** exp3).essence
                for exp4 in range(10):
                    if exp4 not in powers:
                        powers[exp4] = (magic_power ** exp4).essence
                    if powers[exp1] ^ powers[exp2] ^ powers[exp3] ^ powers[exp4] == target:
                        return [exp1, exp2, exp3, exp4]
    
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
    print("[*] Timeout reading response")
s.settimeout(None)

data = data.decode()
print("[DEBUG] Received data:")
print(data)
print("[DEBUG] End of data")

# Parse magic power and dragon life
magic_power_value = None
dragon_life_value = None

lines = data.split('\n')
for i, line in enumerate(lines):
    print(f"[DEBUG] Line {i}: {repr(line[:100])}")
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
spells = solve_dragon_smart(magic_power_value, dragon_life_value)

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

# Read final response
try:
    s.settimeout(2)
    data = s.recv(4096).decode()
    print(data)
except:
    pass

s.close()
