#!/bin/bash

echo "========================================="
echo " Jeanne Hack RPG - Level II Setup"
echo "========================================="
echo

# Check if we're in WSL
if grep -qi microsoft /proc/version; then
    echo "Detected WSL environment"
    echo
fi

# Setup
echo "[1/3] Setting up game files..."
cp "../Jeanne Hack RPG - Level I/jdhack-rpg" . 2>/dev/null || echo "  ⚠️  Game executable not found"
mkdir -p levels
cp level_2.so levels/ 2>/dev/null && echo "  ✓ Level 2 copied to levels/"
cp level_2_patched.so levels/ 2>/dev/null && echo "  ✓ Patched version available"

echo
echo "[2/3] Checking dependencies..."
if command -v ./jdhack-rpg &> /dev/null; then
    echo "  ✓ Game executable found"
else
    echo "  ✗ Game executable missing"
    echo "    Copy from: ../Jeanne Hack RPG - Level I/jdhack-rpg"
fi

if ldconfig -p 2>/dev/null | grep -q ncurses; then
    echo "  ✓ ncurses library found"
else
    echo "  ⚠️  ncurses library may be missing"
    echo "    Install with: sudo apt-get install libncurses5"
fi

echo
echo "[3/3] Running game..."
echo
echo "Commands:"
echo "  Normal:  ./jdhack-rpg --levels ./levels/ --no-sound"
echo "  Patched: cp levels/level_2_patched.so levels/level_2.so && ./jdhack-rpg --levels ./levels/ --no-sound"
echo
echo "For Docker:"
echo "  docker run -it --rm -v \$(pwd):/game ubuntu bash"
echo "  cd /game && apt-get update && apt-get install -y libncurses5"
echo "  ./jdhack-rpg --levels ./levels/ --no-sound"
echo
echo "========================================="
echo

# Check if TERM is set properly
if [ -z "$TERM" ] || [ "$TERM" = "dumb" ]; then
    echo "⚠️  WARNING: TERM not set or set to 'dumb'"
    echo "Try: export TERM=xterm-256color"
    echo
fi

# Try to run if everything looks good
if [ -f "./jdhack-rpg" ] && [ -f "levels/level_2.so" ]; then
    echo "Ready to run! Execute:"
    echo "./jdhack-rpg --levels ./levels/ --no-sound"
fi
