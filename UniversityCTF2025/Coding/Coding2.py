import sys
input = sys.stdin.readline

n = int(input())
baubles = []

for _ in range(n):
    line = input()
    # Parse the line: "identifier: sparkle , stability"
    colon_idx = line.index(':')
    identifier = line[:colon_idx]
    comma_idx = line.index(',', colon_idx)
    sparkle = int(line[colon_idx+2:comma_idx])
    stability = int(line[comma_idx+2:])
    
    # Store as (-sparkle, stability, identifier) for direct sorting
    baubles.append((-sparkle, stability, identifier))

# Sort using default tuple comparison
baubles.sort()

# Print identifiers
sys.stdout.write('\n'.join(bauble[2] for bauble in baubles) + '\n')
