#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class Pad:
    pad: int
    net: Optional[str]


@dataclass
class Footprint:
    reference: Optional[str]
    value: Optional[str]
    raw_lines: List[str]


@dataclass
class Gate:
    gate_type: str
    out_net: str
    input_nets: List[str]


OUTPUT_NETS = [
    "/G59", "/G62", "/G13", "/G19", "/G21", "/G24", "/G26", "/G29", "/G31",
    "/G36", "/G39", "/G41", "/G43", "/G45", "/G47", "/G49", "/G52", "/G54",
    "/G56",
]


def parse_footprints(lines: List[str]) -> List[Footprint]:
    footprints: List[Footprint] = []
    in_fp = False
    depth = 0
    current: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_fp and stripped.startswith("(footprint "):
            in_fp = True
            depth = 0
            current = []
        if in_fp:
            current.append(line)
            depth += line.count("(") - line.count(")")
            if depth == 0:
                reference = None
                value = None
                for fp_line in current:
                    fp_stripped = fp_line.strip()
                    if fp_stripped.startswith('(property "Reference"'):
                        reference = fp_stripped.split('"')[3]
                    elif fp_stripped.startswith('(property "Value"'):
                        value = fp_stripped.split('"')[3]
                footprints.append(Footprint(reference, value, current))
                in_fp = False
    return footprints


def extract_pads(raw_lines: List[str]) -> List[Pad]:
    text = "\n".join(raw_lines)
    pads: List[Pad] = []
    idx = 0
    while True:
        start = text.find("(pad ", idx)
        if start == -1:
            break
        depth = 0
        end = start
        for i in range(start, len(text)):
            ch = text[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0:
                end = i + 1
                break
        block = text[start:end]
        pad_num = None
        net_name = None
        if '(pad "' in block:
            try:
                pad_num = int(block.split('(pad "', 1)[1].split('"', 1)[0])
            except ValueError:
                pad_num = None
        if "(net " in block and '"' in block:
            try:
                net_name = block.split('(net ', 1)[1].split('"', 2)[1]
            except IndexError:
                net_name = None
        if pad_num is not None:
            pads.append(Pad(pad_num, net_name))
        idx = end
    return pads


def build_gates(footprints: Iterable[Footprint], ls27_out6: List[int], ls27_out12: List[int]) -> List[Gate]:
    gates: List[Gate] = []
    for fp in footprints:
        if not fp.reference or not fp.value:
            continue
        if not fp.reference.startswith("U"):
            continue
        pads = {p.pad: p.net for p in extract_pads(fp.raw_lines)}

        def get_net(pin: int) -> Optional[str]:
            return pads.get(pin)

        def add_gate(gate_type: str, out_pin: int, in_pins: List[int]) -> None:
            out_net = get_net(out_pin)
            if not out_net:
                return
            in_nets = [get_net(p) for p in in_pins]
            if any(n is None for n in in_nets):
                return
            gates.append(Gate(gate_type, out_net, [n for n in in_nets if n]))

        match fp.value:
            case "74LS04":
                add_gate("NOT", 2, [1])
                add_gate("NOT", 4, [3])
                add_gate("NOT", 6, [5])
                add_gate("NOT", 8, [9])
                add_gate("NOT", 10, [11])
                add_gate("NOT", 12, [13])
            case "74LS00":
                add_gate("NAND", 3, [1, 2])
                add_gate("NAND", 6, [4, 5])
                add_gate("NAND", 8, [9, 10])
                add_gate("NAND", 11, [12, 13])
            case "74LS02":
                add_gate("NOR", 1, [2, 3])
                add_gate("NOR", 4, [5, 6])
                add_gate("NOR", 10, [8, 9])
                add_gate("NOR", 13, [11, 12])
            case "74LS08":
                add_gate("AND", 3, [1, 2])
                add_gate("AND", 6, [4, 5])
                add_gate("AND", 8, [9, 10])
                add_gate("AND", 11, [12, 13])
            case "74LS32":
                add_gate("OR", 3, [1, 2])
                add_gate("OR", 6, [4, 5])
                add_gate("OR", 8, [9, 10])
                add_gate("OR", 11, [12, 13])
            case "74LS86":
                add_gate("XOR", 3, [1, 2])
                add_gate("XOR", 6, [4, 5])
                add_gate("XOR", 8, [9, 10])
                add_gate("XOR", 11, [12, 13])
            case "74LS21":
                add_gate("AND", 6, [1, 2, 4, 5])
                add_gate("AND", 8, [9, 10, 12, 13])
            case "74LS20":
                add_gate("NAND", 6, [1, 2, 4, 5])
                add_gate("NAND", 8, [9, 10, 12, 13])
            case "74LS27":
                add_gate("NOR", 6, ls27_out6)
                add_gate("NOR", 8, [9, 10, 11])
                add_gate("NOR", 12, ls27_out12)
            case _:
                continue
    return gates


def eval_gates(gates: List[Gate], input_bits: List[int]) -> Dict[str, int]:
    values: Dict[str, int] = {"GND": 0, "+5V": 1}
    for i in range(7):
        values[f"/IN{i}"] = input_bits[i]

    changed = True
    for _ in range(1000):
        if not changed:
            break
        changed = False
        for gate in gates:
            if gate.out_net in values:
                continue
            inputs = [values.get(n) for n in gate.input_nets]
            if any(v is None for v in inputs):
                continue
            if gate.gate_type == "NOT":
                out = 0 if inputs[0] else 1
            elif gate.gate_type == "AND":
                out = 1 if all(v == 1 for v in inputs) else 0
            elif gate.gate_type == "OR":
                out = 1 if any(v == 1 for v in inputs) else 0
            elif gate.gate_type == "NAND":
                out = 0 if all(v == 1 for v in inputs) else 1
            elif gate.gate_type == "NOR":
                out = 0 if any(v == 1 for v in inputs) else 1
            elif gate.gate_type == "XOR":
                out = 0
                for v in inputs:
                    out ^= v
            else:
                continue
            values[gate.out_net] = out
            changed = True
    return values


def score_hits(hits: Dict[str, List[int]]) -> Tuple[int, int, str]:
    single = 0
    printable = 0
    chars: List[str] = []
    for net in OUTPUT_NETS:
        values = hits[net]
        if len(values) == 1:
            single += 1
            code = values[0]
            chars.append(chr(code))
            if 32 <= code <= 126:
                printable += 1
        else:
            chars.append("?")
    return single, printable, "".join(chars)


def find_message(footprints: List[Footprint]) -> str:
    pins = [1, 2, 3, 4, 5, 13]
    best_msg = ""
    best_score = (-1, -1)
    for i in range(len(pins)):
        for j in range(i + 1, len(pins)):
            for k in range(j + 1, len(pins)):
                out6 = [pins[i], pins[j], pins[k]]
                out12 = [p for p in pins if p not in out6]
                gates = build_gates(footprints, out6, out12)
                hits: Dict[str, List[int]] = {n: [] for n in OUTPUT_NETS}
                for val in range(128):
                    bits = [(val >> b) & 1 for b in range(7)]  # IN0 is LSB
                    values = eval_gates(gates, bits)
                    for net in OUTPUT_NETS:
                        if values.get(net) == 1:
                            hits[net].append(val)
                single, printable, msg = score_hits(hits)
                if (single, printable) > best_score:
                    best_score = (single, printable)
                    best_msg = msg
    return best_msg


def main() -> None:
    pcb_path = Path(__file__).with_name("smart-brick-v2.kicad_pcb")
    lines = pcb_path.read_text().splitlines()
    footprints = parse_footprints(lines)
    message = find_message(footprints)
    print(message)


if __name__ == "__main__":
    main()
