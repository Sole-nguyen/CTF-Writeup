#!/usr/bin/env python3
import string
from collections import defaultdict

C = [95,181,145,39,245,91,212,232,123,220,167,69,91,208,245,164,245,145,123,94,62,150,94,172,83,135,96,153,2,208,96,172,201,5,19,131,91,90,53,95,218,238,211,91,4,201,182,135,245,167,74,90,145,96,238]
KNOWN = 'MaytheForcebewithyouyoungpadawanCIT'
UNKNOWN_LEN = 20
FLAG_CHARS = string.ascii_lowercase + '_'

assert len(KNOWN) == 35 and len(C) == 55

ALPHABETS = {
    'lower26': string.ascii_lowercase,
    'upper26': string.ascii_uppercase,
    'alpha27_': string.ascii_lowercase + '_',
    'alpha52_Ul': string.ascii_uppercase + string.ascii_lowercase,
    'alpha52_lU': string.ascii_lowercase + string.ascii_uppercase,
    'base62': string.ascii_uppercase + string.ascii_lowercase + string.digits,
    'print95': ''.join(chr(i) for i in range(32, 127)),
    'ascii256': ''.join(chr(i) for i in range(256)),
}


def encode_char(ch, alpha_name):
    alpha = ALPHABETS[alpha_name]
    if alpha_name == 'lower26':
        ch = ch.lower()
    elif alpha_name == 'upper26':
        ch = ch.upper()
    elif alpha_name == 'alpha27_':
        ch = ch.lower()
        if ch not in string.ascii_lowercase:
            ch = '_'
    if ch not in alpha:
        return None
    return alpha.index(ch)


def decode_idx(idx, alpha_name):
    alpha = ALPHABETS[alpha_name]
    return alpha[idx] if 0 <= idx < len(alpha) else None


def score_text(s):
    good = sum(ch in FLAG_CHARS for ch in s)
    vowels = sum(ch in 'aeiou' for ch in s)
    return good, vowels


def class_a_vig_variants():
    out = []
    for alpha_name, alpha in ALPHABETS.items():
        m = len(alpha)
        p = []
        ok = True
        for ch in KNOWN:
            v = encode_char(ch, alpha_name)
            if v is None:
                ok = False
                break
            p.append(v)
        if not ok:
            continue
        r = [x % m for x in C]
        for model in ('vig', 'beau', 'variant'):
            for L in range(1, 36):
                k = []
                for pi, ri in zip(p, r[:35]):
                    if model == 'vig':
                        k.append((ri - pi) % m)
                    elif model == 'beau':
                        k.append((ri + pi) % m)
                    else:
                        k.append((pi - ri) % m)
                if not all(k[i] == k[i % L] for i in range(35)):
                    continue
                key = k[:L]
                dec = []
                for i in range(35, 55):
                    ri = r[i]
                    kj = key[i % L]
                    if model == 'vig':
                        pi = (ri - kj) % m
                    elif model == 'beau':
                        pi = (kj - ri) % m
                    else:
                        pi = (ri + kj) % m
                    dec.append(decode_idx(pi, alpha_name) or '?')
                dec_s = ''.join(dec)
                out.append((alpha_name, m, model, L, dec_s, score_text(dec_s)))
    return out


def solve_affine_pairs(pairs, m):
    sols = []
    x0, y0 = pairs[0]
    for a in range(m):
        b = (y0 - a * x0) % m
        if all((a * x + b) % m == y for x, y in pairs):
            sols.append((a, b))
    return sols


def class_c_affine_per_pos():
    out = []
    for alpha_name, alpha in ALPHABETS.items():
        m = len(alpha)
        p = []
        ok = True
        for ch in KNOWN:
            v = encode_char(ch, alpha_name)
            if v is None:
                ok = False
                break
            p.append(v)
        if not ok:
            continue
        r = [x % m for x in C]
        for L in range(1, 36):
            params = []
            good = True
            for j in range(L):
                idx = [i for i in range(35) if i % L == j]
                pairs = [(p[i], r[i]) for i in idx]
                sols = solve_affine_pairs(pairs, m)
                if not sols:
                    good = False
                    break
                params.append(sols)
            if not good:
                continue
            # optimistic decode via first solution per position
            dec = []
            amb = 0
            chosen = [s[0] for s in params]
            for i in range(35, 55):
                a, b = chosen[i % L]
                y = r[i]
                cands = []
                for ch in FLAG_CHARS:
                    x = encode_char(ch, 'alpha27_')
                    if x is None or x >= m:
                        continue
                    if (a * x + b) % m == y:
                        cands.append(ch)
                if len(cands) == 1:
                    dec.append(cands[0])
                elif len(cands) == 0:
                    dec.append('?')
                    amb += 1
                else:
                    dec.append('[' + ''.join(cands[:5]) + ('..' if len(cands) > 5 else '') + ']')
                    amb += 1
            out.append((alpha_name, m, L, ''.join(dec), amb))
    return out


def class_b_decimal_digit():
    p = [ord(ch) for ch in KNOWN]
    c = C[:35]
    pd = [[x // 100, (x // 10) % 10, x % 10] for x in p]
    cd = [[x // 100, (x // 10) % 10, x % 10] for x in c]
    hits = []
    for L in range(1, 36):
        # per-digit no carry add/sub
        for mode in ('add_no_carry', 'sub_no_carry'):
            key = [[None] * 3 for _ in range(L)]
            ok = True
            for i in range(35):
                j = i % L
                for d in range(3):
                    k = (cd[i][d] - pd[i][d]) % 10 if mode.startswith('add') else (pd[i][d] - cd[i][d]) % 10
                    if key[j][d] is None:
                        key[j][d] = k
                    elif key[j][d] != k:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                hits.append((mode, L))
        # full mod1000 add/sub
        for mode in ('add_mod1000', 'sub_mod1000'):
            key = [None] * L
            ok = True
            for i in range(35):
                j = i % L
                k = (c[i] - p[i]) % 1000 if mode.startswith('add') else (p[i] - c[i]) % 1000
                if key[j] is None:
                    key[j] = k
                elif key[j] != k:
                    ok = False
                    break
            if ok:
                hits.append((mode, L))
    return hits


def main():
    print('== Class (a)/(d): Vigenere-Beaufort-Variant with residue model ==')
    res_a = class_a_vig_variants()
    nontrivial = [x for x in res_a if x[3] < 35]
    print(f'Total fits: {len(res_a)} | nontrivial period<35 fits: {len(nontrivial)}')
    plausible = [x for x in res_a if x[4].islower() and all(ch in FLAG_CHARS for ch in x[4])]
    plausible.sort(key=lambda x: (x[3], -x[5][1]))
    for row in plausible[:20]:
        print(f'alpha={row[0]:10s} m={row[1]:3d} model={row[2]:8s} L={row[3]:2d} -> {row[4]}')
    if not plausible:
        print('No fully lowercase/underscore candidate outputs found.')

    print('\n== Class (b): decimal-digit polyalphabetic ==')
    hits_b = class_b_decimal_digit()
    if hits_b:
        for h in hits_b:
            print('hit', h)
    else:
        print('No nontrivial period<=35 fit for tested decimal-digit models.')

    print('\n== Class (c): affine-per-key-position on residues ==')
    res_c = class_c_affine_per_pos()
    # show best (lowest ambiguity then shortest period)
    res_c.sort(key=lambda x: (x[4], x[2]))
    for row in res_c[:20]:
        print(f'alpha={row[0]:10s} m={row[1]:3d} L={row[2]:2d} amb={row[4]:2d} -> {row[3]}')


if __name__ == '__main__':
    main()
