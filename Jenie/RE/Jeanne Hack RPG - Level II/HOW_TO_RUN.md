# How to Run Jeanne Hack RPG - Level II

## Prerequisites
- Linux environment with X11 or proper terminal
- ncurses library

## Setup

1. **Copy the game files:**
   ```bash
   # Copy the main game executable from Level I
   cp "../Jeanne Hack RPG - Level I/jdhack-rpg" .
   
   # Create levels directory
   mkdir -p levels
   cp level_2.so levels/
   ```

2. **Run the game:**
   ```bash
   ./jdhack-rpg --levels ./levels/ --no-sound
   ```

## Alternative: Using the Patched Version

If you want to bypass the hash check:

```bash
# Use the patched version
cp level_2_patched.so levels/level_2.so
./jdhack-rpg --levels ./levels/ --no-sound
```

## Using Docker/Container (Recommended)

If you have issues with ncurses:

```bash
docker run -it --rm -v $(pwd):/game ubuntu:latest bash
cd /game
apt-get update && apt-get install -y libncurses5
./jdhack-rpg --levels ./levels/ --no-sound
```

## Troubleshooting

- **"Cannot initialize ressources"**: Your terminal doesn't support ncurses properly
- **"symbol lookup error"**: Missing dependencies, need the full game engine
- **Black screen**: Try a different terminal emulator or SSH session

## What We Know

The flag format is `JDHACK{XXX}` where XXX are 3 binary digits representing achievements.

Most likely flags to try:
- JDHACK{111} (all achievements)
- JDHACK{100}, JDHACK{101}, JDHACK{110}
