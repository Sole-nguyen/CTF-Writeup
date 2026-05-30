# JDHACK RPG - Level I - Complete Solution

## Challenge Analysis

### Step 1: Identify the Binary Functions
Using `nm -D level_1.so`, we found these key functions:
- `enter_village` - The victory function
- `keep_moving_forward` - Contains the password check
- `enc` - Encryption function

### Step 2: Disassemble the Password Check Logic

In the `keep_moving_forward` function at address `0x156d`, the code flow is:

```assembly
1600: call   window_prompt       ; Get user input
1610: call   strdup              ; Duplicate the string  
1618: call   enc                 ; Encrypt the input
1628: lea    0x1156(%rip),%rax   ; Load address 0x2785
162f: mov    %rax,%rdi
1632: call   strcmp              ; Compare encrypted input with target
1637: test   %eax,%eax           ; Check if equal
1639: jne    1661                ; Jump to attack_by_wolves if not equal
165a: call   enter_village       ; Call victory function if equal
```

### Step 3: Analyze the Encryption Function

The `enc` function at address `0x1342`:

```assembly
1354: movzbl (%rax),%eax        ; Load character
1358: xor    $0x1,%eax           ; XOR with 0x1
135e: mov    %eax,%edx
1360: mov    %dl,(%rax)          ; Store back
1366: addq   $0x1,-0x8(%rbp)    ; Next character
136b: movzbl (%rax),%eax
136f: test   %al,%al            ; Check for null terminator
1374: jne    1354                ; Loop
```

**Key Finding:** The encryption is simply XOR with 0x1 for each character!

### Step 4: Extract the Target String

At offset `0x2785` in the binary:
```
B1ofs@urX1t4tswhwDeM2w2m1od
```

### Step 5: Decrypt the Password

Since XOR is reversible (A XOR B XOR B = A), we apply the same operation:

```python
encrypted = "B1ofs@urX1t4tswhwDeM2w2m1od"
password = ''.join(chr(ord(c) ^ 1) for c in encrypted)
# Result: C0ngrAtsY0u5urvivEdL3v3l0ne
```

### Step 6: Verify the Flag Format

The `enter_village` function at `0x14ee` displays:
```c
snprintf(buffer, 0x400, "Congratulations! You can validate with\nJDHACK{%s}", user_input);
```

## Solution

**Password to enter in game:** `C0ngrAtsY0u5urvivEdL3v3l0ne`

**Flag:** `JDHACK{C0ngrAtsY0u5urvivEdL3v3l0ne}`

## Tools Used
- `objdump -d` - Disassembly
- `nm -D` - Dynamic symbols
- `strings` - String extraction
- `dd` - Binary data extraction
- Python - XOR decryption

## Key Takeaways
1. The password check uses a simple XOR cipher with key 0x1
2. User input is encrypted then compared with a stored encrypted string
3. The flag is constructed from the original (unencrypted) user input
