# obfpyscated

`meow.py` is a two-layer obfuscation. The outer layer XORs a bytes literal with `2`, producing a script that loads a `marshal` payload XORed with `27`. That payload connects to `meow.sylvie.fyi`, fetches `/static/suspicious_among_us`, and decrypts it with AES-GCM using a key derived by XORing an embedded bytes literal with `55`.

The decrypted payload is another marshaled program. It fetches `/static/ritsec_catgirl.png`, then uses a hardcoded list of pixel coordinates. For each coordinate `(x, y)`, it XORs the RGB components and converts the result to a character. Concatenating those characters yields the flag.

**Flag:** `RS{1f_y0u_r4n_th47_0n_y0ur_h0s7_y0u_sh0uld_m4k3_b3tter_d3cis1on5}`
