# RITSEC CTF - Reverse Engineering Challenges

This directory contains solutions for 4 reverse engineering challenges from RITSEC CTF.

## Challenges Overview

### 1. Deadwater ✓ SOLVED
**Difficulty:** Hard  
**Category:** Reverse Engineering / Cryptography

A challenge involving a TSX-protected custom hashing algorithm.

- **Files:** `deadwater` (x86-64 binary), `solve.py`, `writeup.md`
- **Solution:** Reimplemented PRNG and inverted validation
- **Flag:** `RITSEC{52f8c23363f6e22fe711e30879413706db0c2cf209de2044d16f79e13f01c0518f3414a0642d4823}`

```bash
cd Deadwater
python3 solve.py  # Outputs the hex string
echo "52f8c23363f6e22fe711e30879413706db0c2cf209de2044d16f79e13f01c0518f3414a0642d4823" | ./deadwater
# Output: yarrr
```

---

### 2. Buried Treasure ✓ SOLVED
**Difficulty:** Medium  
**Category:** Reverse Engineering / Encryption

Multi-layer encrypted binary with XOR and RC4 protection.

- **Files:** `buried_treasure` (x86-64 binary), `solve.py`, `writeup.md`
- **Solution:** Sequential layer extraction (XOR → XOR → RC4)
- **Layers:** 3 layers with embedded 16-byte keys at offset 0x240

```bash
cd Buried_Treasure
python3 solve.py  # Extracts real_final_binary
chmod +x real_final_binary
./real_final_binary  # Flag checker binary
```

**Decryption Chain:**
1. Layer 1: XOR decryption → layer2_binary
2. Layer 2: XOR decryption → layer3_binary  
3. Layer 3: RC4 decryption → final_binary

---

### 3. Black Ledger ⚠️ PARTIAL
**Difficulty:** Medium  
**Category:** Reverse Engineering (ARM64)

ARM aarch64 binary requiring a 32-character input ("captain's 32-rune course").

- **Files:** `black_ledger` (ARM64 binary), `solve.py`, `writeup.md`
- **Challenge:** Binary validation of 32-char string
- **Decoy:** Contains fake string `zo21_parrot_loot_fake_way_out_xx`

```bash
cd Black_Ledger
# Requires ARM64 analysis tools or qemu-aarch64
qemu-aarch64 -L /usr/aarch64-linux-gnu ./black_ledger
# Or use Ghidra/IDA Pro with ARM64 support
```

**Analysis Required:**
- Static analysis with Ghidra/IDA Pro (ARM64 support)
- Identify the correct 32-character validation string
- Flag format: `RITSEC{[32-character-string]}`

---

### 4. Marauder Matchup ⚠️ PARTIAL
**Difficulty:** Medium  
**Category:** Reverse Engineering / pwn (ARM64)

Network service running ARM64 binary with process management.

- **Files:** `arsenal` (ARM64 binary), `solve.py`, `writeup.md`
- **Service:** `nc marauder.ctf.ritsec.club 1112`
- **Goal:** Find and kill enemy process by PID

```bash
cd Marauder_Matchup
python3 solve.py  # Connects to service
# Or manually:
nc marauder.ctf.ritsec.club 1112
```

**Analysis Required:**
- Reverse engineer ARM64 `arsenal` binary
- Understand getpid/kill logic
- Identify enemy PID and send correct kill command

---

## Tools Required

### For All Challenges:
- Python 3
- pwntools (`pip install pwntools`)
- strings, objdump, file

### For ARM64 Challenges (Black Ledger, Marauder):
- Ghidra or IDA Pro with ARM64 support
- qemu-aarch64 (optional for emulation)
- ARM64 cross-tools

## Quick Start

```bash
# Install dependencies
pip install pwntools

# Run solved challenges
cd Deadwater && python3 solve.py
cd Buried_Treasure && python3 solve.py

# Analyze ARM64 challenges
cd Black_Ledger && python3 solve.py  # Shows analysis steps
cd Marauder_Matchup && python3 solve.py  # Connects to service
```

## Results Summary

| Challenge | Status | Flag Available | Tools Needed |
|-----------|--------|----------------|--------------|
| Deadwater | ✓ Complete | Yes | Python, strings |
| Buried Treasure | ✓ Complete | Partial* | Python, file |
| Black Ledger | ⚠️ Partial | No | ARM64 tools |
| Marauder Matchup | ⚠️ Partial | No | ARM64 tools, network |

*Buried Treasure extracts the final binary; flag requires further RE of the checker.

## Author Notes

- **Deadwater**: Excellent cryptographic RE challenge with custom PRNG
- **Buried Treasure**: Creative multi-layer onion encryption  
- **Black Ledger & Marauder**: Require ARM64 emulation or cross-platform tools

---

For detailed writeups, see the `writeup.md` file in each challenge directory.
