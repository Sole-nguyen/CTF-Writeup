from __future__ import annotations

import re
import builtins
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Minimal evaluators for the constant expressions used in baby.py.
# These obfuscated helpers all reduce to XOR for the places we use them.

def G0g0sQu1D_116510(a: int, b: int) -> int:
    return a ^ b


def g0GOsquiD(a: int, b: int) -> int:
    return a ^ b


def gOg0sQuId(a: int, b: int) -> int:
    return a ^ b


def G0G0SQU1D(a: int, b: int) -> int:
    return a ^ b


@dataclass(frozen=True)
class SliceConstraint:
    start: int
    end: int
    value: str


class SliceProxy:
    """A placeholder for g0go[start:end] that survives further slicing and captures equality."""

    def __init__(self, constraints: list[SliceConstraint], start: int, end: int, *, reversed_view: bool = False):
        self._constraints = constraints
        self.start = int(start)
        self.end = int(end)
        self.reversed_view = bool(reversed_view)

    def __len__(self) -> int:  # just in case
        return max(0, self.end - self.start)

    def __getitem__(self, sl: slice | int) -> "SliceProxy | str":
        # baby.py only ever does slicing like [::-1] or [::step].
        if isinstance(sl, int):
            # Return a dummy char-like value.
            return "?"
        if sl.step is not None and sl.step < 0:
            # Reversal doesn't change the region in the original input, so keep start/end.
            return SliceProxy(self._constraints, self.start, self.end, reversed_view=not self.reversed_view)
        return SliceProxy(self._constraints, self.start, self.end, reversed_view=self.reversed_view)

    def __eq__(self, other: object) -> bool:
        # Capture constraints when compared against a concrete string.
        if isinstance(other, str):
            # If the *view* was reversed before comparison, then the underlying slice
            # in the original input must be the reverse of what we're being compared to.
            val = other[::-1] if self.reversed_view else other
            self._constraints.append(SliceConstraint(self.start, self.end, val))
            return True
        if isinstance(other, SliceProxy):
            # Slice-vs-slice comparisons don't directly constrain content; treat as satisfied.
            return True
        return False

    def __repr__(self) -> str:
        suf = " (reversed)" if self.reversed_view else ""
        return f"<SliceProxy {self.start}:{self.end}{suf}>"


class TrackedInput:
    """Pretends to be the user input string, but yields SliceProxy slices."""

    def __init__(self, constraints: list[SliceConstraint], n: int):
        self._constraints = constraints
        self._n = int(n)

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, key: slice | int) -> Any:
        if isinstance(key, int):
            return "?"
        start = 0 if key.start is None else int(key.start)
        stop = self._n if key.stop is None else int(key.stop)
        return SliceProxy(self._constraints, start, stop)

    def __repr__(self) -> str:
        return f"<TrackedInput len={self._n}>"


def extract_expected_len_expr(src: str) -> str:
    # Find `if len(g0go) == <expr>:`
    m = re.search(r"len\(g0go\)\s*==\s*(.+?):\s*(?:\n|$)", src)
    if not m:
        raise RuntimeError("Couldn't find len(g0go) == ... check")
    return m.group(1).strip()


def reconstruct(n: int, constraints: list[SliceConstraint]) -> str:
    buf = ["?"] * n
    for c in constraints:
        if c.end <= c.start:
            continue
        if c.end > n:
            continue
        expected = c.value
        if len(expected) != (c.end - c.start):
            # Some comparisons may be between transformed strings; skip mismatched lengths.
            continue
        for i, ch in enumerate(expected):
            pos = c.start + i
            if 0 <= pos < n:
                if buf[pos] not in ("?", ch):
                    # Conflict: keep the first, but note.
                    pass
                else:
                    buf[pos] = ch
    return "".join(buf)


def main() -> None:
    baby_path = Path(__file__).with_name("baby.py")
    src = baby_path.read_text(encoding="utf-8", errors="replace")

    len_expr = extract_expected_len_expr(src)

    # Evaluate expected length using XOR-only semantics.
    env = {
        "G0g0sQu1D_116510": G0g0sQu1D_116510,
        "g0GOsquiD": g0GOsquiD,
        "gOg0sQuId": gOg0sQuId,
        "G0G0SQU1D": G0G0SQU1D,
    }
    expected_len = eval(len_expr, {"__builtins__": {}}, env)
    if not isinstance(expected_len, int):
        raise RuntimeError(f"Expected length is not int: {expected_len!r}")

    constraints: list[SliceConstraint] = []

    # Run baby.py with a hooked input() that returns our TrackedInput.
    # This causes all slice==string checks to record the expected substring.
    def fake_input(_prompt: str = "") -> TrackedInput:
        return TrackedInput(constraints, expected_len)

    # Keep regular builtins but override input.
    builtins_override = builtins.__dict__.copy()
    builtins_override["input"] = fake_input

    g: dict[str, Any] = {"__builtins__": builtins_override, "__name__": "__main__"}
    exec(compile(src, str(baby_path), "exec"), g, g)

    # Now reconstruct the flag candidate.
    candidate = reconstruct(expected_len, constraints)

    print(f"[+] expected length: {expected_len}")
    print(f"[+] captured constraints: {len(constraints)}")
    print(candidate)


if __name__ == "__main__":
    main()
