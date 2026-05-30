#!/usr/bin/env python3
# Usage: python3 match_libc_base.py /path/to/libc.so.6 leaks.txt
# leaks.txt: one hex address per line (e.g. 0x7ffcee42c830)

import sys, os, subprocess, struct
from elftools.elf.elffile import ELFFile

if len(sys.argv) < 3:
    print("Usage: python3 match_libc_base.py /path/to/libc.so.6 leaks.txt")
    sys.exit(1)

libc_path = sys.argv[1]
leaks_file = sys.argv[2]

# load libc symbols
f = open(libc_path, 'rb')
elf = ELFFile(f)
symtab = {}
# collect dynamic symbols
if elf.get_section_by_name('.dynsym'):
    sec = elf.get_section_by_name('.dynsym')
    for sym in sec.iter_symbols():
        name = sym.name
        if not name: continue
        addr = sym['st_value']
        symtab[name] = addr
# also use .symtab if present
if elf.get_section_by_name('.symtab'):
    sec = elf.get_section_by_name('.symtab')
    for sym in sec.iter_symbols():
        name = sym.name
        if not name: continue
        addr = sym['st_value']
        symtab.setdefault(name, addr)

# symbols of interest (expandable)
interesting = ['printf','puts','__libc_start_main','read','fgets','system','__libc_start_main','memcpy','write','close','open']

candidates = []
leaks = []
with open(leaks_file) as L:
    for line in L:
        line = line.strip()
        if not line: continue
        try:
            leaks.append(int(line,16))
        except:
            print("Skipping invalid line:", line)

print("Loaded %d symbols from libc, %d leaks to test\n" % (len(symtab), len(leaks)))

# Build a filtered list of symbols to try (interesting ∪ top libc exported)
symlist = []
for name, off in symtab.items():
    if name in interesting or name.startswith('g')==False:
        symlist.append((name, off))
# ensure interesting ones come first
symlist_sorted = sorted(symlist, key=lambda x: (0 if x[0] in interesting else 1, x[0]))

def is_page_aligned(x):
    return (x & 0xfff) == 0

# For each leak and each symbol compute candidate base
for leak in leaks:
    for name, off in symlist_sorted:
        if off == 0:
            continue
        base = leak - off
        # sanity checks: base should be non-negative and page-aligned-ish (or at least plausible)
        if base <= 0: 
            continue
        # check if base + off == leak
        if (base + off) != leak:
            # sometimes leak may be in the middle of function (leak points into .text)
            # Accept if (base < leak < base + filesize)
            pass
        # quick heuristic: libc typical mapping in high mem: 0x7f...
        if (leak >> 40) not in (0x7f, 0x00):
            # still consider but mark lower priority
            score = 1
        else:
            score = 0
        candidates.append((score, leak, name, hex(off), hex(base)))
# sort candidates by score then leak
candidates = sorted(candidates, key=lambda x: (x[0], x[1]))
print("Potential matches (score 0 = likely libc addr highmem):")
for c in candidates[:200]:
    print("leak=%#x sym=%s sym_off=%s base_candidate=%s" % (c[1], c[2], c[3], c[4]))

# Also print top unique bases (grouped)
bases = {}
for _, leak, name, soff, base in candidates:
    bases.setdefault(base, []).append((hex(leak), name, soff))
print("\nDistinct candidate bases and supporting leaks (showing up to 10 bases):")
count = 0
for base, lst in sorted(bases.items(), key=lambda x: -len(x[1])):
    print("%s  (supported by %d leaks)" % (base, len(lst)))
    for entry in lst[:6]:
        print("   leak=%s sym=%s sym_off=%s" % entry)
    count += 1
    if count >= 10: break

f.close()
