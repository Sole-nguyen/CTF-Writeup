import json
import traceback
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

from crypto import decrypt
from filter_cipher import NLFFilterCipher, WG_ANF_TERMS

# Use sage's BooleanPolynomialRing for faster algebraic solving
try:
    from sage.all import *
except ImportError:
    print("Sage not available, falling back to brute force")
    from itertools import product


@dataclass(frozen=True)
class Challenge:
    L: int
    feedback_taps: Tuple[int, ...]
    filter_taps: Tuple[int, ...]
    keystream: Tuple[int, ...]
    nonce_hex: str
    ct_hex: str


def load_challenge(path: str) -> Challenge:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    return Challenge(
        L=int(obj["L"]),
        feedback_taps=tuple(obj["feedback_taps"]),
        filter_taps=tuple(obj["filter_taps"]),
        keystream=tuple(obj["keystream"]),
        nonce_hex=obj["nonce"],
        ct_hex=obj["ct"],
    )


def solve_with_sage(chal: Challenge) -> List[int]:
    """Try to solve using Sage's Groebner basis"""
    print("Using Sage for algebraic solving...")
    
    # Create Boolean polynomial ring
    R = BooleanPolynomialRing(chal.L, ['s' + str(i) for i in range(chal.L)])
    state_vars = [R.gen(i) for i in range(chal.L)]
    
    equations = []
    state = list(state_vars)
    
    for t, out_bit in enumerate(chal.keystream):
        # Get tapped bits
        taps = [state[i] for i in chal.filter_taps]
        
        # Evaluate ANF for WG filter
        z = 0
        for mon in WG_ANF_TERMS:
            prod = 1
            for idx in mon:
                prod = prod * taps[idx]
            z = z + prod
        
        # Add equation
        equations.append(z + out_bit)
        
        # Compute feedback
        fb = sum([state[i] for i in chal.feedback_taps])
        state = [fb] + state[:-1]
    
    print(f"Solving {len(equations)} polynomial equations...")
    I = ideal(equations)
    G = I.groebner_basis()
    
    print(f"Groebner basis has {len(G)} elements")
    
    # Extract solution
    V = I.variety()
    if not V:
        raise RuntimeError("No solution found")
    
    print(f"Found {len(V)} solution(s)")
    sol = V[0]
    
    bits = [int(sol.get(R.gen(i), 0)) for i in range(chal.L)]
    return bits


def brute_force_partial(chal: Challenge, num_bits_to_guess: int = 20) -> List[int]:
    """Brute force first few bits and use constraint propagation"""
    print(f"Brute forcing first {num_bits_to_guess} bits...")
    
    from itertools import product
    
    best_match = 0
    best_state = None
    
    for guess in product([0, 1], repeat=num_bits_to_guess):
        # Try to extend this guess
        state = list(guess) + [0] * (chal.L - num_bits_to_guess)
        
        # Check how many keystream bits match
        test_state = state[:]
        matches = 0
        
        for t, expected_bit in enumerate(chal.keystream):
            # Compute output
            taps = [test_state[i] for i in chal.filter_taps]
            
            z = 0
            for mon in WG_ANF_TERMS:
                prod = 1
                for idx in mon:
                    prod &= taps[idx]
                    if prod == 0:
                        break
                z ^= prod
            
            if z == expected_bit:
                matches += 1
            
            # Clock LFSR
            fb = 0
            for idx in chal.feedback_taps:
                fb ^= test_state[idx]
            test_state = [fb] + test_state[:-1]
        
        if matches > best_match:
            best_match = matches
            best_state = state[:]
            print(f"  Guess {guess[:5]}... matches {matches}/{len(chal.keystream)}")
            
            if matches == len(chal.keystream):
                return best_state
    
    print(f"Best match: {best_match}/{len(chal.keystream)}")
    return best_state if best_state else [0] * chal.L


def try_decrypt_with_bits(chal: Challenge, bits: List[int]) -> bytes:
    nonce = bytes.fromhex(chal.nonce_hex)
    ct = bytes.fromhex(chal.ct_hex)
    return decrypt(nonce, ct, bits)


def verify_keystream(chal: Challenge, bits: List[int]) -> bool:
    c = NLFFilterCipher(chal.feedback_taps, chal.filter_taps, bits)
    ks = c.keystream(len(chal.keystream))
    return list(ks) == list(chal.keystream)


def main() -> None:
    here = Path(__file__).resolve().parent
    try:
        chal = load_challenge(str(here / "challenge.json"))

        try:
            bits = solve_with_sage(chal)
        except (ImportError, NameError):
            print("Sage not available, trying brute force...")
            bits = brute_force_partial(chal, num_bits_to_guess=16)
        
        recovered = "".join(map(str, bits))
        ks_ok = verify_keystream(chal, bits)

        (here / "recovered_state.txt").write_text(
            recovered + "\n",
            encoding="utf-8",
        )
        (here / "verify.txt").write_text(
            f"keystream_matches={ks_ok}\n",
            encoding="utf-8",
        )

        if not ks_ok:
            print("WARNING: Keystream doesn't match!")
            return

        # Attempt decryption
        candidates = [
            ("direct", bits),
            ("reversed", list(reversed(bits))),
        ]

        errs: List[str] = []
        for name, cand in candidates:
            try:
                pt = try_decrypt_with_bits(chal, cand)
            except Exception as e:
                errs.append(f"{name}: {type(e).__name__}: {e}")
                continue

            (here / "flag.txt").write_bytes(pt)
            (here / "decrypt_mode.txt").write_text(name + "\n", encoding="utf-8")
            print(f"Flag: {pt.decode('utf-8', errors='ignore')}")
            return

        (here / "decrypt_errors.txt").write_text("\n".join(errs) + "\n", encoding="utf-8")
        raise RuntimeError("All decryption attempts failed.")
    except Exception:
        (here / "run_error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
