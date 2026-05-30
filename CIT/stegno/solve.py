import re

def decode_zwc_stego(text):
    # Mapping the invisible characters to their Base-4 values
    # Based on the sequence found in your flag.txt
    zwc_map = {
        '\u200c': 0,  # Zero Width Non-Joiner
        '\u200d': 1,  # Zero Width Joiner
        '\u202c': 2,  # Pop Directional Formatting
        '\ufeff': 3,  # Zero Width No-Break Space (BOM)
        '\u202d': 3,  # Left-to-Right Override
        '\u202f': 3   # Narrow No-Break Space
    }

    # Extract all Zero-Width and formatting characters
    pattern = r'[\u200b-\u200f\u202a-\u202f\ufeff\u2060]'
    hidden_chars = "".join(re.findall(pattern, text))

    # Split into blocks of 8 characters
    blocks = [hidden_chars[i:i+8] for i in range(0, len(hidden_chars), 8)]
    
    flag = ""
    for block in blocks:
        if len(block) < 8: continue
        
        # The first 5 chars are the 'wall' header; we decode the last 3
        d1 = zwc_map.get(block[5], 0)
        d2 = zwc_map.get(block[6], 0)
        d3 = zwc_map.get(block[7], 0)
        
        # Base 64 + (Base-4 calculation)
        ascii_val = 64 + (d1 * 16) + (d2 * 4) + d3
        flag += chr(ascii_val)
        
    return flag

# The content from your flag.txt
data = """‌‌‌‌‍‌‌﻿‌‌‌‌‍‌‬‍‌‌‌‌‍‍‍‌‌‌‌‌‍﻿‬﻿Another ‌‌‌‌‍‬﻿﻿year‌‌‌‌‍‬‬﻿‌‌‌‌‍‍﻿﻿, ‌‌‌‌‍‬﻿‍another‌‌‌‌‍‬‌‍ ‌‌‌‌‍﻿‬‍steg challenge.. Something-‌‌‌‌‍‬‌‬something‌‌‌‌‍‬‍‍ the flag is‌‌‌‌‍‍﻿﻿ hidden ‌‌‌‌‍‬﻿‬in‌‌‌‌‍‬﻿﻿‌‌‌‌‍﻿‍‌‌‌‌‌‍‍﻿﻿ plain ‌‌‌‌‍﻿‌‌sight‌‌‌‌‍‬﻿‌,‌‌‌‌‍‬‌‍ but I'll‌‌‌‌‍‬‬‍ leave it up ‌‌‌‌‍‬﻿‬to you to see‌‌‌‌‍‍﻿﻿ if‌‌‌‌‍﻿‌﻿‌‌‌‌‍‬‬‍ that really‌‌‌‌‍‬‍﻿‌‌‌‌‍‬‬‌ is‌‌‌‌‍﻿‍‌ true or‌‌‌‌‍﻿﻿‍ not!"""

print(f"Decoded Flag: {decode_zwc_stego(data)}")
