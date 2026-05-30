# Guess My Pokemon! - Crypto Challenge Writeup

**CTF:** Jeanne d'Hack CTF  
**Category:** Cryptography  
**Challenge URL:** http://crypto.jeanne-hack-ctf.org:5001  
**Flag:** `JDHACK{T1m3_b4$3d_53cR3t5_Ar3_r3411y_b4d}`

## Challenge Description

> Would you find the secret Pokemon chosen by the server? An encrypted hint is given to you to achieve this...
>
> That's not a Web challenge, the app is only here to provide a more user-friendly experience. The flag can be obtained only by finding the correct Pokemon, don't try to pwn the Web server. A proof-of-work mechanism protects against brute-force attempts, so there's no point in trying ;)

## Initial Reconnaissance

The challenge presents a web application where we need to guess a Pokemon in 3 tries. An encrypted hint is provided, but the encryption key is not known to us.

### API Endpoints Discovered

From analyzing the source code (`api.php`), the following endpoints are available:

- `GET /api/game` - Get current game state
- `POST /api/guess` - Submit a Pokemon guess (requires PoW)
- `POST /api/new` - Start a new game (requires PoW)
- `GET /api/pow-challenge` - Get proof-of-work challenge
- `GET /api/uptime` - Get game duration

### Key Observations

1. **Encryption:** The Pokemon name is encrypted using AES-256-CBC
2. **Encrypted Hint:** The server provides an encrypted version of the target Pokemon
3. **Proof-of-Work:** A PoW mechanism prevents brute-force guessing
4. **Encrypted Guess:** When we make a guess, the server returns its encrypted value

## Vulnerability Analysis

### The Weak Key Generation

Looking at the encryption function in `api.php`:

```php
function encryptPokemonName($pokemonName) {
    $key = $_SESSION["aes_key"];
    $iv = random_bytes(16);
    
    $encrypted = openssl_encrypt(
        $pokemonName,
        'AES-256-CBC',
        $key,
        OPENSSL_RAW_DATA,
        $iv
    );
    
    $combined = $iv . $encrypted;
    return base64_encode($combined);
}
```

The AES key is generated during game initialization:

```php
$_SESSION['aes_key'] = hash('sha256', uniqid(), true);
$_SESSION['game_start_time'] = (int)time();
```

### Critical Vulnerability: Predictable Key Generation

The vulnerability lies in using PHP's `uniqid()` function:

1. **`uniqid()` Format:** PHP's `uniqid()` returns a string in the format `sprintf("%08x%05x", seconds, microseconds)`
   - 8 hex digits for the current second timestamp
   - 5 hex digits for microseconds (0-999999)

2. **Information Leak:** The API response includes `game_start_timestamp`, which is the exact Unix timestamp when the game started

3. **Limited Entropy:** Since we know the timestamp, we only need to bruteforce the microsecond component (1 million possibilities)

### Attack Vector

This is a **time-based key recovery attack**:

1. Get the encrypted hint from `/api/game`
2. Extract the `game_start_timestamp` from the API response
3. Bruteforce all possible `uniqid()` values for that timestamp
4. For each candidate, derive the AES key and attempt decryption
5. Valid Pokemon names will decrypt successfully
6. Submit the correct Pokemon to get the flag

## Exploitation

### Step 1: Retrieve Game State

```python
import requests
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BASE_URL = "http://crypto.jeanne-hack-ctf.org:5001/api"
session = requests.Session()

# Get game state
state = session.get(f"{BASE_URL}/game").json()
encrypted_hint_b64 = state['game']['encrypted_hint']
game_start_timestamp = state['game_start_timestamp']

# Decode encrypted hint
encrypted_data = base64.b64decode(encrypted_hint_b64)
iv = encrypted_data[:16]
ciphertext = encrypted_data[16:]
```

### Step 2: Bruteforce the Key

```python
for usec in range(0, 1000000):
    # Reconstruct uniqid() value
    uniq = f"{game_start_timestamp:08x}{usec:05x}"
    
    # Generate AES key (same as PHP: hash('sha256', $uniq, true))
    key = hashlib.sha256(uniq.encode()).digest()
    
    try:
        # Attempt decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted, 16)
        pokemon = plaintext.decode('utf-8', errors='ignore')
        
        # Check if it's a valid Pokemon name
        if pokemon.isalpha() and pokemon[0].isupper():
            print(f"Found: {pokemon}")
            # Make guess...
    except:
        pass
```

### Step 3: Solve Proof-of-Work and Submit Guess

```python
def solve_pow(challenge, difficulty):
    prefix = '0' * difficulty
    nonce = 0
    while True:
        test_hash = hashlib.sha256(f"{challenge}{nonce}".encode()).hexdigest()
        if test_hash.startswith(prefix):
            return nonce, test_hash
        nonce += 1

# Get PoW challenge
pow_resp = session.get(f"{BASE_URL}/pow-challenge").json()
nonce, hash_result = solve_pow(pow_resp['challenge'], pow_resp['difficulty'])

# Submit guess
guess_resp = session.post(f"{BASE_URL}/guess", json={
    'guess': pokemon,
    'pow': {
        'challenge': pow_resp['challenge'],
        'nonce': nonce,
        'hash': hash_result
    }
}).json()

if guess_resp.get('correct'):
    print(f"FLAG: {guess_resp.get('flag')}")
```

## Solution

Running the complete exploit:

```bash
$ python3 exploit2.py
Game start timestamp: 1769790436
Encrypted hint: YttK5+ae9rfqtsq76mlikkWxwuXl9ZAFGRmiNzUKU88=

Bruteforcing AES key from uniqid()...
Tested 0/1000000 microseconds...
Tested 50000/1000000 microseconds...
...
✅ Found valid decryption!
Pokemon: Roggenrola
uniqid: 697cdbe47b991
Microseconds: 506257

Solving proof-of-work...
PoW solved with nonce=475748

Guessing: Roggenrola
🎉 CORRECT! FLAG: JDHACK{T1m3_b4$3d_53cR3t5_Ar3_r3411y_b4d}
```

**Answer:** Roggenrola  
**Flag:** `JDHACK{T1m3_b4$3d_53cR3t5_Ar3_r3411y_b4d}`

## Key Takeaways

### Vulnerability Summary

- **CWE-338:** Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)
- **Root Cause:** Using time-based functions (`uniqid()`) as cryptographic key material
- **Impact:** Complete key recovery leading to decryption of all encrypted data

### Lessons Learned

1. **Never use time-based functions for cryptographic keys**
   - `uniqid()` is predictable and has limited entropy
   - Use cryptographically secure random functions like `random_bytes()`

2. **Don't leak timing information**
   - The `game_start_timestamp` provided the exact time needed for the attack
   - Avoid exposing precise timing data that could aid attackers

3. **Proper key generation**
   ```php
   // BAD ❌
   $key = hash('sha256', uniqid(), true);
   
   // GOOD ✅
   $key = random_bytes(32);  // For AES-256
   ```

4. **Defense in depth**
   - Even with PoW protection, the weak key generation was exploitable
   - Multiple layers of security are important, but fundamentals must be solid

### Flag Message Analysis

The flag `T1m3_b4$3d_53cR3t5_Ar3_r3411y_b4d` directly confirms the vulnerability: "Time-based secrets are really bad" - a perfect reminder of the security principle violated in this challenge.

## Complete Exploit Code

See `exploit2.py` for the full working exploit.

## Tools Used

- Python 3
- `requests` - HTTP client
- `pycryptodome` - AES decryption
- `hashlib` - SHA256 hashing and PoW solving

---

*Writeup by: [Your Handle]*  
*Date: 2026-01-30*
