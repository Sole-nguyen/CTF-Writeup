from __future__ import annotations

from pathlib import Path


def G0g0sQu1D_116510(a: int, b: int) -> int:
    return a ^ b


def g0GOsquiD(a: int, b: int) -> int:
    return a ^ b


def gOg0sQuId(a: int, b: int) -> int:
    return a ^ b


def g0gosqu1D(vals: list[int], key: int) -> str:
    # In baby.py this ultimately reduces to: ''.join(chr(v ^ key) for v in vals)
    return "".join(chr(v ^ key) for v in vals)


def extract_success_expr(src: str) -> str:
    lines = src.splitlines()

    # Find the first success-print: `if g0GOsqU1d:` then `print(g0gosqu1D(...))`
    start_idx = None
    for i, line in enumerate(lines):
        if "if g0GOsqU1d" in line:
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError("Couldn't find `if g0GOsqU1d` in baby.py")

    # Find the first print after that
    print_idx = None
    for j in range(start_idx, min(start_idx + 200, len(lines))):
        if "print(g0gosqu1D" in lines[j].replace(" ", ""):
            print_idx = j
            break
    if print_idx is None:
        # fallback: global first occurrence
        for j, line in enumerate(lines):
            if line.lstrip().startswith("print(g0gosqu1D"):
                print_idx = j
                break
    if print_idx is None:
        raise RuntimeError("Couldn't find success print(g0gosqu1D(...))")

    # Collect a full expression possibly spanning multiple lines by paren counting.
    chunk = ""
    paren = 0
    started = False
    for k in range(print_idx, len(lines)):
        line = lines[k]
        if not started:
            # Start at first 'print(' occurrence in this line
            p = line.find("print(")
            if p == -1:
                continue
            line = line[p + len("print(") :]
            started = True
        chunk += line + "\n"
        paren += line.count("(") - line.count(")")
        if started and paren <= 0:
            break

    # chunk currently includes trailing ')' from print(...) and maybe spaces/newlines.
    # Strip everything after the matching end, and remove surrounding whitespace.
    chunk = chunk.strip()

    # If it ends with a ')' from print call, drop the final ')'
    if chunk.endswith(")"):
        chunk = chunk[:-1].rstrip()

    return chunk


def main() -> None:
    baby_path = Path(__file__).with_name("baby.py")
    src = baby_path.read_text(encoding="utf-8", errors="replace")

    expr = extract_success_expr(src)

    # Evaluate in a restricted environment: only our tiny helpers
    env = {
        "G0g0sQu1D_116510": G0g0sQu1D_116510,
        "g0GOsquiD": g0GOsquiD,
        "gOg0sQuId": gOg0sQuId,
        "g0gosqu1D": g0gosqu1D,
    }

    result = eval(expr, {"__builtins__": {}}, env)
    print(result)


if __name__ == "__main__":
    main()
