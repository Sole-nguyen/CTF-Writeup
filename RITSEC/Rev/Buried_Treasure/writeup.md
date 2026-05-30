# Buried Treasure

## Challenge Description
A reverse engineering challenge involving multiple layers of encryption/obfuscation.

## Analysis
The `buried_treasure` binary contains multiple encrypted layers that need to be extracted sequentially:

1. **Layer 1** - buried_treasure → XOR decryption
2. **Layer 2** - hidden_binary → XOR decryption  
3. **Layer 3** - layer3_binary → RC4 decryption
4. **Final** - final_binary → Executable that validates the flag

Each layer uses an encryption key embedded at offset 0x240 (16 bytes).

### Decryption Process

**XOR Layers (1 & 2):**
- Key location: offset 0x240
- Data location: offset 0x465
- Method: Simple XOR with 16-byte repeating key

**RC4 Layer (3):**
- Key location: offset 0x240
- Data location: offset 0x485
- Size: 0x512F8 bytes
- Method: RC4 stream cipher

## Solution

The solve script performs the following steps:

1. Extract Layer 1 using XOR with key at 0x240
2. Extract Layer 2 using XOR with key at 0x240  
3. Extract Layer 3 using RC4 with key at 0x240
4. Run the final binary to check flag validation logic

The final binary is a flag checker that validates user input.

## Tools Used
- Python 3
- RC4 implementation
- Hex editor for offset analysis

## Flag
The flag can be obtained by:
1. Running the extraction script
2. Reverse engineering the final binary to understand the validation logic
3. Extracting or brute-forcing the correct input

Format: RITSEC{...}
