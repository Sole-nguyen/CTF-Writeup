#!/usr/bin/env python3
import socket
import hashlib
import string
from functools import lru_cache
import random

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

# Try random search + greedy approach
def solve_dragon_random(magic_power_value, dragon_life_value):
    magic_power = QuantumNimber(magic_power_value)
    target = dragon_life_value
    
    print(f"[*] Computing powers up to 200...")
    powers = {}
    for i in range(200):
        powers[i] = (magic_power ** i).essence
        if i < 10 or (i < 50 and i % 5 == 0):
            print(f"    power[{i}] has {powers[i].bit_length()} bits")
    
    # Try systematic search with larger range
    print(f"[*] Systematic search for 4-combination...")
    
    # Use greedy: find best single power first
    best_match = None
    best_dist = target.bit_length()
    
    for i in range(min(200, len(powers))):
        xor_result = target ^ powers[i]
        if xor_result == 0:
            print(f"[*] Found 1-spell solution: [{i}]")
            return [i]
        dist = xor_result.bit_length()
        if dist < best_dist:
            best_dist = dist
            best_match = (i, xor_result)
    
    if best_match:
        i1, remaining1 = best_match
        print(f"[*] Best single: {i1}, remaining has {remaining1.bit_length()} bits")
        
        # Find best second power
        best_match2 = None
        best_dist2 = remaining1.bit_length()
        for i in range(min(200, len(powers))):
            xor_result = remaining1 ^ powers[i]
            if xor_result == 0:
                print(f"[*] Found 2-spell solution: [{i1}, {i}]")
                return [i1, i]
            dist = xor_result.bit_length()
            if dist < best_dist2:
                best_dist2 = dist
                best_match2 = (i, xor_result)
        
        if best_match2:
            i2, remaining2 = best_match2
            print(f"[*] Best second: {i2}, remaining has {remaining2.bit_length()} bits")
            
            # Find best third power
            for i in range(min(200, len(powers))):
                xor_result = remaining2 ^ powers[i]
                if xor_result == 0:
                    print(f"[*] Found 3-spell solution: [{i1}, {i2}, {i}]")
                    return [i1, i2, i]
            
            # Find fourth power
            for i in range(min(200, len(powers))):
                for j in range(min(200, len(powers))):
                    xor_result = remaining2 ^ powers[i] ^ powers[j]
                    if xor_result == 0:
                        print(f"[*] Found 4-spell solution: [{i1}, {i2}, {i}, {j}]")
                        return [i1, i2, i, j]
    
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

# Read response
print("[*] Reading response after PoW...")
data = b''
s.settimeout(5)
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
        print(f"[*] Magic Power value parsed")
    if "Dragon's Life Force:" in line:
        dragon_life_value = int(line.split(':')[1].strip())
        print(f"[*] Dragon Life value parsed")

if not magic_power_value or not dragon_life_value:
    print("[!] Could not parse values")
    s.close()
    exit(1)

# Solve
print("[*] Solving...")
spells = solve_dragon_random(magic_power_value, dragon_life_value)

if spells:
    print(f"[*] Solution: {spells}")
    while len(spells) < 4:
        spells.append(0)
    
    for i, spell in enumerate(spells[:4]):
        print(f"[*] Spell {i+1}: {spell}")
        s.sendall((str(spell) + '\n').encode())
        try:
            data = s.recv(4096).decode()
            print(data)
        except:
            pass
else:
    print("[!] No solution found")
    s.close()
    exit(1)

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
