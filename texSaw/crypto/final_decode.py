#!/usr/bin/env python3

ciphertext = """Azza wfahv ztu. N rnvy, bndfah na zbfaztv vztak, n vztak ndfa uz n dcnqza zw n uzlvfa, icfuv nmztu. Nthtvutv, rgz gnv gnk n mnk afhgu, vfuv ty mcfadfah nak ytwmcfak. Zg rgnu rnv ugnu rzwk (fv gfv ugzthgu) ugnu wna ugwzthg bp mwnfa ncc afhgu, ugnu fkfzufl rzwk ugnu, gnwk nv F'k uwp uz yta fu kzra, rnv ncrnpv etvu na falg zw urz ztu zi bp hwnvy - izrc zw iztc zw Szr zw Szpnc? - n rzwk rgflg, mp nvvzlfnufza, mwzthgu fauz ycnp na falzahwtztv bnvv nak bnhbn zi aztav, fkfzbv, vczhnav nak vnpfahv, n lzaitvfah, nbzwygztv ztuyztwfah rgflg F vzthgu fa snfa uz lzauwzc zw utwa zii mtu rgflg rztak nwztak bp bfak n rgfwcrfak zi n lzwk, n rgfycnvg zi n lzwk, n lzwk ugnu rztck vycfu nhnfa nak nhnfa, rztck dafu nhnfa nak nhnfa, zi rzwkv rfugztu lzbbtaflnufza zw nap yzvvfmfcfup zi lzbmfanufza, rzwkv rfugztu ywzanalfnufza, vfhafiflnufza zw uwnavlwfyufza mtu ztu zi rgflg, azurfugvunakfah, rnv mwzthgu izwug n ictq, n lzaufatztv, lzbynlu nak ctlfk iczr: na fautfufza, n snlfccnufah iwfvvza zi fcctbfanufza nv fi lnthgu fa n icnvg zi cfhguafah zw fa n bfvu nmwtyucp wfvfah uz tavgwztk na zmsfztv vfha - mtu n vfha, ncnv, ugnu rztck cnvu na favunau zacp uz snafvg izw hzzk."""

# Looking at "Azza" - if this is "Noon", then z=o, a=n
# Looking at common patterns more carefully:
# "ztu" = "out" gives z=o, t=u, u=t? No that's circular
# Let me reconsider: Maybe "ztu" = "out" means z=o, t=u, u=t? That doesn't work
# Or maybe z=o, t=u but 'u' in cipher = 't' in plain? Let's reconsider

# "ugnu" appears a lot - this should be "that"
# So: u=t, g=h, a=a, t=n? But 'a' in cipher = 'a' in plain seems unlikely for substitution

# Let me try: cipher -> plain
cipher_to_plain = {}

# I'll use a different approach - recognize this might be from a famous text
# "Azza wfahv ztu" could be "Noon rings out"
# If "Azza" = "Noon": A->N, z->o, a->n
# But that makes two mappings from 'a', so 'A'->N (capital), small 'a'->n

# Let's be more careful. In substitution ciphers, each letter maps to exactly one other
# I notice: cipher has repeated patterns

# Let me try to match "that" pattern
# "ugnu" most likely = "that": u->t, g->h, a->a?, t->t? No, let me think...
# Actually: u->t, g->h, n->a, u->t matches! So cipher 'n' -> plain 'a'

# "nak" = "and": n->a, a->n, k->d
# Wait, that gives n->a and a->n which is impossible in simple substitution

# Let me reconsider. Simple substitution means: each cipher letter maps to ONE plain letter
# "ugnu" if it's "that": u->t, g->h, n->a, u->t (consistent!)
# "nak" if it's "and": n->a, a->n, k->d
# But we have n->a from above, so if "nak"[1] is 'a' in cipher, it should map to 'a' in plain
# So "nak" = "a?d" where ?=a gives "aad" - not "and"
# So "nak" might not be "and". Let me look at other patterns.

# Actually, looking at "na" appearing frequently - this is likely "an" or "in"
# If "na" = "an", then n->a, a->n

# So we have from "ugnu"="that": u->t, g->h, n->a, u->t ✓
# And from "na"="an": n->a ✓, a->n ✓  
# And from "nak"="and": n->a ✓, a->n ✓, k->d ✓

# Great! So:  u->t, g->h, n->a, a->n, k->d

# Let me build the full mapping more carefully
mapping = {
    'a': 'n',
    'b': 'm',
    'c': 'l',
    'd': 'k',
    'e': 'j',
    'f': 'i',
    'g': 'h',
    'h': 'g',
    'i': 'f',
    'k': 'd',
    'l': 'c',
    'n': 'a',
    'p': 'y',
    'q': 'z',
    'r': 'w',
    's': 'v',
    't': 'u',
    'u': 't',
    'v': 's',
    'w': 'r',
    'x': 'x',
    'y': 'p',
    'z': 'o',
}

def decode(text, mapping):
    result = []
    for char in text:
        if char.lower() in mapping:
            new_char = mapping[char.lower()]
            if char.isupper():
                result.append(new_char.upper())
            else:
                result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)

decoded = decode(ciphertext, mapping)
print(decoded)
