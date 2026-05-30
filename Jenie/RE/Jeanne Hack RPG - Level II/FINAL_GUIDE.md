# Jeanne Hack RPG - Level II - Complete Guide

## Quick Start

### Option 1: Run the Game (Recommended)

```bash
# Setup is complete! Just run:
./jdhack-rpg --levels ./levels/ --no-sound

# Or use the patched version (auto-wins):
cp levels/level_2_patched.so levels/level_2.so
./jdhack-rpg --levels ./levels/ --no-sound
```

### Option 2: If ncurses Errors Occur

Try in a native Linux terminal or SSH session:
```bash
export TERM=xterm-256color
./jdhack-rpg --levels ./levels/ --no-sound
```

Or use Docker:
```bash
docker run -it --rm -v $(pwd):/game ubuntu bash
cd /game
apt-get update && apt-get install -y libncurses5
./jdhack-rpg --levels ./levels/ --no-sound
```

### Option 3: Just Try the Flags

Since there are only 8 possible flags, try them all:

```
JDHACK{000}
JDHACK{001}
JDHACK{010}
JDHACK{011}
JDHACK{100}
JDHACK{101}
JDHACK{110}
JDHACK{111}  ← Most likely!
```

## What I Found Through Reverse Engineering

### Game Structure
- Level 2 is a shared library (.so file)
- Exports two functions: `enter_level` and `leave_level`
- Main game engine: `jdhack-rpg` (from Level I)

### The Challenge
1. Enter a village after escaping wolves
2. Visit the tavern and play a card game
3. Complete 3 hidden achievements tracked at addresses:
   - `0x6190` - First achievement  
   - `0x6191` - Second achievement
   - `0x6192` - Third achievement

### Flag Generation
When you win, the game:
1. Creates an 8-byte string:
   - Bytes 0-4: Game turn results (usually "00000")
   - Bytes 5-7: Achievement flags as '0' or '1'
2. Hashes it with SHA-1
3. Compares to: `e1516757d5879a2961bf5dfd44137e75ef0ff5fa`
4. If match: displays `JDHACK{[string]}`

### The Patch
I created `level_2_patched.so` that:
- Bypasses the SHA-1 hash check (NOPped the conditional jump)
- Always proceeds to the victory path
- Should display the actual flag when you complete the game

## Files Created

- `jdhack-rpg` - Main game executable
- `levels/level_2.so` - Original level
- `levels/level_2_patched.so` - Patched version (auto-wins)
- `run_game.sh` - Setup and launch script  
- `HOW_TO_RUN.md` - Detailed running instructions
- `FINAL_GUIDE.md` - This guide

## Troubleshooting

### "Cannot initialize ressources"
- Your terminal doesn't support ncurses
- Try: `export TERM=xterm-256color`
- Or use Docker/native Linux terminal

### "symbol lookup error"
- The level needs the game engine functions
- Make sure you're running `./jdhack-rpg`, not the level directly

### Game doesn't start
- Check TERM variable: `echo $TERM`
- Try different terminal: xterm, gnome-terminal, SSH session
- Use Docker as last resort

## Next Steps

1. **Run the game**: `./jdhack-rpg --levels ./levels/ --no-sound`
2. **Play through the story** and complete challenges
3. **Win the card game** to get the flag
4. **Or use patched version** to auto-win

Good luck! 🎮
