zen_void.bin is mostly emptiness.

Stage 8: find the non-zero 'island' inside the correct void range and apply the 1-byte key.
Key (hex): 0x2a

Stage 9: another island exists. Its key is derived from what you found in stage 8:
  key = sum(bytes(stage8_text)) % 256

One void range contains a decoy island.

aux lane notes (diagnostic):
  lane-17 = 0e121e6d54284c38c1caa1d1dc9699f18ff1f98cef9edcdd
