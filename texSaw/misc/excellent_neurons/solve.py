#!/usr/bin/env python3
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_to_idx(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n


def parse_ref(ref: str) -> tuple[int, int]:
    m = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    if not m:
        raise ValueError(f"Bad cell ref: {ref}")
    return int(m.group(2)), col_to_idx(m.group(1))


def load_cells(xlsx_path: str, sheet_xml: str = "xl/worksheets/sheet2.xml") -> dict[tuple[int, int], float | str | None]:
    with zipfile.ZipFile(xlsx_path) as zf:
        root = ET.fromstring(zf.read(sheet_xml))

    cells: dict[tuple[int, int], float | str | None] = {}
    for c in root.findall(".//s:sheetData/s:row/s:c", NS):
        ref = c.attrib["r"]
        r, ci = parse_ref(ref)
        v = c.find("s:v", NS)
        if v is None:
            cells[(r, ci)] = None
            continue
        text = v.text or ""
        try:
            cells[(r, ci)] = float(text)
        except ValueError:
            cells[(r, ci)] = text
    return cells


def get_num(cells: dict, r: int, c: int) -> float:
    val = cells.get((r, c), 0)
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    return 0.0


def extract_params(cells: dict):
    C, AF, BJ = 3, 32, 62

    # Layer1: input(30) -> hidden1(60)
    W1 = [[get_num(cells, rr, cc) for cc in range(C, AF + 1)] for rr in range(11, 71)]
    b1 = [get_num(cells, 75, cc) for cc in range(C, BJ + 1)]

    # Layer2: hidden1(60) -> hidden2(1)
    W2 = [get_num(cells, 87, cc) for cc in range(C, BJ + 1)]
    b2 = get_num(cells, 92, 3)

    # Layer3: hidden2(1) -> output(4)
    W3 = [get_num(cells, 101, cc) for cc in range(3, 7)]
    b3 = [get_num(cells, 104, cc) for cc in range(3, 7)]

    return W1, b1, W2, b2, W3, b3


def forward(chars: list[str], W1, b1, W2, b2, W3, b3):
    # Excel uses D8:AG8 for 30 characters; empty cell -> 0 in normalized input
    x = [0.0 if ch == "" else ord(ch) / 127.0 for ch in chars]

    z1 = [sum(x[j] * W1[i][j] for j in range(30)) + b1[i] for i in range(60)]
    a1 = [v if v > 0 else 0.0 for v in z1]

    z2 = sum(a1[i] * W2[i] for i in range(60)) + b2
    a2 = z2 if z2 > 0 else 0.0

    z3 = [a2 * W3[k] + b3[k] for k in range(4)]
    a3 = [1.0 / (1.0 + math.exp(-v)) for v in z3]

    is_flag = (a3[0] > 0.5) and (a3[1] < 0.5) and (a3[2] > 0.5) and (a3[3] < 0.5)
    return z2, a2, z3, a3, is_flag


def derive_best_string(W1, b1, W2):
    # Important observation:
    # Each input position feeds exactly two 1-sparse neurons in layer1,
    # so z2 can be maximized per-position independently.
    by_pos: dict[int, list[tuple[float, float, float]]] = defaultdict(list)
    for i, row in enumerate(W1):
        nz = [(j, w) for j, w in enumerate(row) if abs(w) > 1e-12]
        if len(nz) == 1:
            j, w = nz[0]
            by_pos[j].append((w, b1[i], W2[i]))

    allowed = [chr(i) for i in range(32, 127)] + [""]
    best_chars: list[str] = []

    for pos in range(30):
        best_score = -1e100
        best_char = ""
        for ch in allowed:
            x = 0.0 if ch == "" else ord(ch) / 127.0
            s = 0.0
            for w, b, v in by_pos[pos]:
                z = w * x + b
                a = z if z > 0 else 0.0
                s += v * a
            if s > best_score:
                best_score = s
                best_char = ch
        best_chars.append(best_char)

    return best_chars


def main():
    cells = load_cells("challenge.xlsx")
    W1, b1, W2, b2, W3, b3 = extract_params(cells)

    best_chars = derive_best_string(W1, b1, W2)
    z2, a2, z3, a3, ok = forward(best_chars, W1, b1, W2, b2, W3, b3)

    raw = "".join(best_chars)
    flag = raw[: raw.index("}") + 1] if "}" in raw else raw.rstrip()

    print("[+] Candidate:", flag)
    print("[+] z2 =", z2, "a2 =", a2)
    print("[+] a3 =", a3)
    print("[+] Condition (F>0.5,L<0.5,A>0.5,G<0.5):", ok)


if __name__ == "__main__":
    main()
