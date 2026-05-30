import requests
import json
import hashlib
import sys

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
        if nonce % 100000 == 0:
            print(f"Testing nonce {nonce}...", file=sys.stderr)

def get_pow():
    """Get proof-of-work challenge"""
    resp = session.get(f"{BASE_URL}/pow-challenge")
    data = resp.json()
    print(f"PoW Challenge: difficulty={data['difficulty']}", file=sys.stderr)
    nonce, hash_result = solve_pow(data['challenge'], data['difficulty'])
    print(f"PoW Solved: nonce={nonce}", file=sys.stderr)
    return {
        'challenge': data['challenge'],
        'nonce': nonce,
        'hash': hash_result
    }

def get_game_state():
    """Get current game state"""
    resp = session.get(f"{BASE_URL}/game")
    return resp.json()

def make_guess(pokemon, pow_data):
    """Make a guess and return encrypted value"""
    resp = session.post(f"{BASE_URL}/guess", json={
        'guess': pokemon,
        'pow': pow_data
    })
    return resp.json()

# Get initial game state and encrypted hint
print("Getting game state...", file=sys.stderr)
state = get_game_state()
encrypted_hint = state['game']['encrypted_hint']
print(f"Encrypted hint: {encrypted_hint}", file=sys.stderr)

# Load Pokemon list (using common ones first for efficiency)
common_pokemon = [
    "Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee",
    "Mewtwo", "Mew", "Charizard", "Blastoise", "Venusaur"
]

# Try to find the Pokemon by comparing encrypted values
print("\nStarting chosen-plaintext attack...", file=sys.stderr)

for pokemon in common_pokemon:
    print(f"\nTrying {pokemon}...", file=sys.stderr)
    pow_data = get_pow()
    result = make_guess(pokemon, pow_data)
    
    if 'encrypted_guess' in result:
        encrypted_guess = result['encrypted_guess']
        print(f"Encrypted guess: {encrypted_guess}", file=sys.stderr)
        
        # Compare with hint
        if encrypted_guess == encrypted_hint:
            print(f"\n🎉 MATCH FOUND! The Pokemon is: {pokemon}", file=sys.stderr)
            if result.get('correct'):
                print(f"\n✅ CORRECT! Flag: {result.get('flag', 'N/A')}")
                sys.exit(0)
    
    if result.get('correct'):
        print(f"\n✅ Got it! Flag: {result.get('flag', 'N/A')}")
        sys.exit(0)
    
    # Check if game is over
    if result.get('game', {}).get('game_over'):
        print("\n❌ Game over, need to start new game", file=sys.stderr)
        break

print("\n❌ Didn't find the Pokemon in common list", file=sys.stderr)
