import requests
import json
import hashlib
import sys
import base64
from Crypto.Cipher import AES

BASE_URL = "http://crypto.jeanne-hack-ctf.org:5001/api"
session = requests.Session()

def solve_pow(challenge, difficulty):
    """Solve proof-of-work challenge"""
    prefix = '0' * difficulty
    nonce = 0
    while True:
        test_hash = hashlib.sha256(f"{challenge}{nonce}".encode()).hexdigest()
        if test_hash.startswith(prefix):
            return nonce, test_hash
        nonce += 1

def get_pow():
    """Get proof-of-work challenge"""
    resp = session.get(f"{BASE_URL}/pow-challenge")
    data = resp.json()
    nonce, hash_result = solve_pow(data['challenge'], data['difficulty'])
    return {
        'challenge': data['challenge'],
        'nonce': nonce,
        'hash': hash_result
    }

# Get game state
state = session.get(f"{BASE_URL}/game").json()
encrypted_hint_b64 = state['game']['encrypted_hint']

# Decode the encrypted hint
encrypted_hint = base64.b64decode(encrypted_hint_b64)
iv_hint = encrypted_hint[:16]
ciphertext_hint = encrypted_hint[16:]

print(f"Encrypted hint length: {len(ciphertext_hint)} bytes")
print(f"This suggests Pokemon name has ~{len(ciphertext_hint)} bytes (with padding)")

# The vulnerability: we can see the ciphertext length which reveals info about plaintext length
# AES block size is 16 bytes. With PKCS7 padding:
# - 1-16 bytes plaintext -> 16 bytes ciphertext
# - 17-32 bytes plaintext -> 32 bytes ciphertext

ciphertext_len = len(ciphertext_hint)
if ciphertext_len == 16:
    print("Pokemon name is 1-15 characters (likely short name)")
elif ciphertext_len == 32:
    print("Pokemon name is 16-31 characters (longer name)")

# Common Pokemon by length - let's filter
print("\nTrying to guess based on ciphertext length...")

# However, we still need the key to decrypt. Let me look for another vulnerability...
# Wait! The IV is prepended to the ciphertext. This is standard, but let's see if there's
# a timing attack or oracle we can exploit.

# Actually, looking at the code again: we get 3 guesses. The key is in the SESSION
# which we don't have access to. Each encryption uses a new random IV.

# Let me try a different approach: use the encrypted_guess feature to test candidates
print("\nUsing binary search approach with multiple games...")

# Read all Pokemon from a list
all_pokemon = []
try:
    with open('pokemon.txt', 'r') as f:
        all_pokemon = [line.strip() for line in f if line.strip()]
except:
    # Generate a comprehensive list
    all_pokemon = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon",
                   "Charizard", "Squirtle", "Wartortle", "Blastoise", "Pikachu",
                   "Raichu", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Mewtwo",
                   "Mew", "Snorlax", "Dragonite", "Gyarados"]

# Filter by length based on ciphertext
target_min_len = (ciphertext_len - 16) if ciphertext_len > 16 else 1
target_max_len = ciphertext_len - 1
candidates = [p for p in all_pokemon if target_min_len <= len(p) <= target_max_len]

print(f"Candidates ({len(candidates)}): {candidates[:10]}...")

# Brute force with new games
for pokemon in candidates[:50]:  # Try top 50 candidates
    # Start new game
    pow_data = get_pow()
    new_game = session.post(f"{BASE_URL}/new", json={'pow': pow_data})
    
    if new_game.status_code != 200:
        print(f"Failed to start new game: {new_game.text}")
        continue
    
    # Make a guess
    pow_data = get_pow()
    result = session.post(f"{BASE_URL}/guess", json={
        'guess': pokemon,
        'pow': pow_data
    }).json()
    
    if result.get('correct'):
        print(f"\n🎉 FOUND IT! Pokemon: {pokemon}")
        print(f"Flag: {result.get('flag', 'N/A')}")
        sys.exit(0)
    
    print(f"Tried {pokemon} - Wrong")

print("\n❌ Pokemon not found in candidate list")
