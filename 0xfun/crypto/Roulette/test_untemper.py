#!/usr/bin/env python3
import random

# Test the untemper function
def untemper(y):
    """Reverse the tempering transformation of MT19937"""
    y = int(y)
    
    # Invert y ^= (y >> 18)
    y ^= (y >> 18)
    
    # Invert y ^= (y << 15) & 0xEFC60000
    y ^= (y << 15) & 0xEFC60000
    
    # Invert y ^= (y << 7) & 0x9D2C5680
    for i in range(4):
        y ^= (y << 7) & 0x9D2C5680
    
    # Invert y ^= (y >> 11)
    y ^= (y >> 11)
    y ^= (y >> 22)
    
    return y & 0xFFFFFFFF

# Test it
rng = random.Random(12345)
for _ in range(10):
    val = rng.getrandbits(32)
    # Try to untemper and see if we can recover the state
    print(f"Generated: {val}")

# Now let's verify the untemper function by creating a new RNG and checking
print("\nTesting untemper:")
rng2 = random.Random(12345)
state = rng2.getstate()[1][:624]
print(f"First state value: {state[0]}")

# Generate first value and try to untemper it
rng3 = random.Random(12345)
val = rng3.getrandbits(32)
print(f"First generated value: {val}")

# Try to untemper - but we need the tempered version
# The MT19937 state is untempered, so we can't directly compare
