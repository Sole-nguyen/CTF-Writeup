import json
import traceback
from pathlib import Path
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import z3

from crypto import decrypt
from filter_cipher import NLFFilterCipher, WG_ANF_TERMS


@dataclass(frozen=True)
class Challenge:
    L: int
    feedback_taps: Tuple[int, ...]
    filter_taps: Tuple[int, ...]
    keystream: Tuple[int, ...]
    nonce_hex: str
    ct_hex: str


def xor_bools(xs: Sequence[z3.BoolRef]) -> z3.BoolRef:
    acc: z3.BoolRef = z3.BoolVal(False)
    for x in xs:
        acc = z3.Xor(acc, x)
    return acc


def anf_eval_z3(taps: Sequence[z3.BoolRef], terms: Sequence[Tuple[int, ...]]) -> z3.BoolRef:
    """Evaluate ANF (xor of monomials, each monomial is and of selected taps)."""
    acc: z3.BoolRef = z3.BoolVal(False)
    for mon in terms:
        if not mon:
            mon_val = z3.BoolVal(True)
        else:
            mon_val = taps[mon[0]]
            for idx in mon[1:]:
                mon_val = z3.And(mon_val, taps[idx])
        acc = z3.Xor(acc, mon_val)
    return acc


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


def solve_state_bits(chal: Challenge, terms: Sequence[Tuple[int, ...]] = WG_ANF_TERMS) -> List[int]:
    # state[0] is newest bit (matches filter_cipher.NLFFilterCipher).
    state = [z3.Bool(f"s0_{i}") for i in range(chal.L)]

    s = z3.Solver()

    for t, out_bit in enumerate(chal.keystream):
        taps = [state[i] for i in chal.filter_taps]
        z = anf_eval_z3(taps, terms)
        s.add(z == z3.BoolVal(bool(out_bit)))

        fb = xor_bools([state[i] for i in chal.feedback_taps])
        state = [fb] + state[:-1]

    print(f"Solving with {len(chal.keystream)} constraints over {chal.L} bits...")
    if s.check() != z3.sat:
        raise RuntimeError("No solution (UNSAT) — modeling mismatch?")

    print("Found solution, extracting bits...")
    m = s.model()
    bits = [1 if z3.is_true(m.eval(z3.Bool(f"s0_{i}"), model_completion=True)) else 0 for i in range(chal.L)]
    return bits


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

        bits = solve_state_bits(chal)
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

        # Attempt decryption. If it fails due to an interpretation mismatch, try common flips.
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
            return

        (here / "decrypt_errors.txt").write_text("\n".join(errs) + "\n", encoding="utf-8")
        raise RuntimeError("All decryption attempts failed.")
    except Exception:
        (here / "run_error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
