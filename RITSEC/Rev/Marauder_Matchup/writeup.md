# Marauder Matchup

## Challenge Description
There's an opposing ship that just snuck up on us! They seem to have gotten a head start one before us. Can you find their pid and kill it before they do us in? We'll reward you handsomely.

Author: @chasek

nc marauder.ctf.ritsec.club 1112

## Analysis
The challenge provides:
- A remote service at `marauder.ctf.ritsec.club:1112`
- An ARM64 binary called `arsenal`

When connecting to the service, it prints "interpreting" and waits for input.

### Binary Analysis (arsenal)
- **Architecture:** ARM aarch64, static-pie linked
- **System calls used:** `getpid`, `kill`
- **Strings found:** References to process operations, pid validation

The binary appears to:
1. Get its own PID
2. Possibly spawn or interact with another process
3. Expect you to find and kill the enemy process before it kills yours

## Solution Approach

1. **Connect to the service:**
   ```bash
   nc marauder.ctf.ritsec.club 1112
   ```

2. **Reverse engineer the ARM64 binary:**
   - Use Ghidra or IDA Pro with ARM64 support
   - Analyze the logic involving `getpid()` and `kill()`
   - Understand what input the binary expects

3. **Find the enemy PID:**
   - The binary likely provides information about process IDs
   - Identify which PID represents the "enemy ship"

4. **Kill the correct process:**
   - Send the kill command with the correct PID
   - The flag is revealed upon success

## Tools Used
- netcat
- Ghidra/IDA Pro (ARM64 support)
- pwntools (optional)

## Flag
Format: RITSEC{...}

The flag is obtained by successfully identifying and killing the enemy process before it terminates your connection.
