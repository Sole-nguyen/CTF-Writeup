#!/usr/bin/env python3
import ast
import math
import re
from collections import Counter
from functools import reduce
from pathlib import Path


def parse_logbook(path: Path):
    text = path.read_text()
    match = re.search(r"Log: (\[.*\])\nCiphertext: ([0-9a-f]+)", text, re.S)
    if not match:
        raise ValueError("logbook format not recognized")
    log = ast.literal_eval(match.group(1))
    ctext = bytes.fromhex(match.group(2))
    return log, ctext


def recover_modulus(log):
    diffs = []
    for i in range(len(log) - 3):
        d1 = log[i + 1] - log[i]
        d2 = log[i + 2] - log[i + 1]
        d3 = log[i + 3] - log[i + 2]
        val = d3 * d1 - d2 * d2
        if val:
            diffs.append(abs(val))

    gcds = []
    for i in range(len(diffs)):
        for j in range(i + 1, len(diffs)):
            g = math.gcd(diffs[i], diffs[j])
            if g.bit_length() > 200:
                gcds.append(g)
        if len(gcds) >= 2000:
            break

    if not gcds:
        raise ValueError("failed to recover modulus")

    modulus = reduce(math.gcd, gcds)
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        while modulus % p == 0:
            modulus //= p
    return modulus


def recover_heads(log, modulus):
    counter = Counter()
    for i in range(1, len(log) - 1):
        s0, s1, s2 = log[i - 1], log[i], log[i + 1]
        d = (s1 - s0) % modulus
        if d == 0:
            continue
        a = ((s2 - s1) % modulus) * pow(d, -1, modulus) % modulus
        b = (s1 - a * s0) % modulus
        counter[(a, b)] += 1

    heads = [ab for ab, count in counter.most_common() if count > 1]
    if not heads:
        raise ValueError("failed to recover heads")
    return heads


def recover_states(log, heads, modulus):
    states = []
    for i in range(1, len(log)):
        s_prev, s_curr = log[i - 1], log[i]
        matches = [
            idx
            for idx, (a, b) in enumerate(heads)
            if (a * s_prev + b) % modulus == s_curr
        ]
        if len(matches) != 1:
            raise ValueError("ambiguous head assignment")
        states.append(matches[0])
    return states


def transition_probs(states, n):
    counts = [[0] * n for _ in range(n)]
    for i in range(len(states) - 1):
        counts[states[i]][states[i + 1]] += 1
    probs = [[0.0] * n for _ in range(n)]
    for i in range(n):
        total = sum(counts[i])
        if total == 0:
            continue
        for j in range(n):
            probs[i][j] = counts[i][j] / total
    return probs


def generate_candidates(ctext, heads, modulus, start_sval):
    prefix_charset = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
    inside_charset = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")

    nodes = [(start_sval, st, b"", []) for st in range(len(heads))]
    for pos in range(len(ctext)):
        new_nodes = []
        for s, st, plain, seq in nodes:
            a, b = heads[st]
            s_next = (a * s + b) % modulus
            pbyte = ctext[pos] ^ (s_next & 0xFF)

            if pos == len(ctext) - 1 and pbyte != ord("}"):
                continue

            if pbyte == ord("{"):
                if b"{" in plain:
                    continue
            else:
                if b"{" not in plain:
                    if pbyte not in prefix_charset:
                        continue
                else:
                    if pbyte == ord("}") and pos != len(ctext) - 1:
                        continue
                    if pbyte not in inside_charset and not (
                        pos == len(ctext) - 1 and pbyte == ord("}")
                    ):
                        continue

            for nxt in range(len(heads)):
                new_nodes.append((s_next, nxt, plain + bytes([pbyte]), seq + [st]))
        nodes = new_nodes

    return [
        (plain, seq)
        for _s, _st, plain, seq in nodes
        if b"{" in plain and plain.endswith(b"}")
    ]


def pick_best(candidates, probs, last_state):
    best = None
    for plain, seq in candidates:
        p0 = probs[last_state][seq[0]]
        if p0 == 0:
            continue
        logp = math.log(p0)
        ok = True
        for i in range(len(seq) - 1):
            p = probs[seq[i]][seq[i + 1]]
            if p == 0:
                ok = False
                break
            logp += math.log(p)
        if not ok:
            continue
        if best is None or logp > best[0]:
            best = (logp, plain)
    return best[1] if best else None


def main():
    log, ctext = parse_logbook(Path("logbook.txt"))
    modulus = recover_modulus(log)
    heads = recover_heads(log, modulus)
    states = recover_states(log, heads, modulus)
    probs = transition_probs(states, len(heads))

    start_sval = log[-1]
    candidates = generate_candidates(ctext, heads, modulus, start_sval)
    flag = pick_best(candidates, probs, states[-1])
    if not flag:
        raise SystemExit("no flag found")
    print(flag.decode())


if __name__ == "__main__":
    main()
