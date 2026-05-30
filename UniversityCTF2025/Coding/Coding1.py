# Flickering Snowglobe - Count stable segments
# A stable segment is a maximal contiguous sequence of the same character

# Read input
n = int(input())
s = input().strip()

# Count stable segments
if not s:
    print(0)
else:
    count = 1  # Start with 1 segment
    for i in range(1, len(s)):
        if s[i] != s[i-1]:  # Character changed, new segment
            count += 1
    
    print(count)
