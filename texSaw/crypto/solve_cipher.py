import re
from collections import Counter

ciphertext = """Azza wfahv ztu. N rnvy, bndfah na zbfaztv vztak, n vztak ndfa uz n dcnqza zw n uzlvfa, icfuv nmztu. Nthtvutv, rgz gnv gnk n mnk afhgu, vfuv ty mcfadfah nak ytwmcfak. Zg rgnu rnv ugnu rzwk (fv gfv ugzthgu) ugnu wna ugwzthg bp mwnfa ncc afhgu, ugnu fkfzufl rzwk ugnu, gnwk nv F'k uwp uz yta fu kzra, rnv ncrnpv etvu na falg zw urz ztu zi bp hwnvy - izrc zw iztc zw Szr zw Szpnc? - n rzwk rgflg, mp nvvzlfnufza, mwzthgu fauz ycnp na falzahwtztv bnvv nak bnhbn zi aztav, fkfzbv, vczhnav nak vnpfahv, n lzaitvfah, nbzwygztv ztuyztwfah rgflg F vzthgu fa snfa uz lzauwzc zw utwa zii mtu rgflg rztak nwztak bp bfak n rgfwcrfak zi n lzwk, n rgfycnvg zi n lzwk, n lzwk ugnu rztck vycfu nhnfa nak nhnfa, rztck dafu nhnfa nak nhnfa, zi rzwkv rfugztu lzbbtaflnufza zw nap yzvvfmfcfup zi lzbmfanufza, rzwkv rfugztu ywzanalfnufza, vfhafiflnufza zw uwnavlwfyufza mtu ztu zi rgflg, azurfugvunakfah, rnv mwzthgu izwug n ictq, n lzaufatztv, lzbynlu nak ctlfk iczr: na fautfufza, n snlfccnufah iwfvvza zi fcctbfanufza nv fi lnthgu fa n icnvg zi cfhguafah zw fa n bfvu nmwtyucp wfvfah uz tavgwztk na zmsfztv vfha - mtu n vfha, ncnv, ugnu rztck cnvu na favunau zacp uz snafvg izw hzzk."""

# Frequency analysis
freq = Counter(ciphertext.lower())
print("Most common characters:", freq.most_common(20))

# Common English letter frequencies suggest this is a simple substitution
# Let's try some common patterns:
# Single letters: N, F (likely "a" or "I")
# Common 2-letter words: zi, zw, ztu, np, nv, fa, fy, uz, zw
# Common 3-letter words: ugnu (likely "that")

# Looking at patterns:
# "ugnu" appears frequently - likely "that"
# "nak" appears frequently - likely "and"
# Single "N" at start - likely "A"
# Single "F" - likely "I"

# Let's build a substitution mapping
mapping = {}

# From "ugnu" = "that"
mapping['u'] = 't'
mapping['g'] = 'h'
mapping['n'] = 'a'
# mapping['t'] already used, so skip

# From "nak" = "and"
mapping['k'] = 'd'

# Common patterns
mapping['f'] = 'i'
mapping['z'] = 'o'
mapping['w'] = 'r'

# More analysis
mapping['v'] = 's'
mapping['r'] = 'w'
mapping['y'] = 'p'
mapping['m'] = 'b'
mapping['c'] = 'l'
mapping['q'] = 'z'
mapping['l'] = 'c'
mapping['e'] = 'j'
mapping['t'] = 'n'
mapping['h'] = 'g'
mapping['d'] = 'k'
mapping['a'] = 'n'
mapping['i'] = 'f'
mapping['s'] = 'v'
mapping['x'] = 'x'
mapping['b'] = 'm'
mapping['p'] = 'y'

def decode(text, mapping):
    result = []
    for char in text:
        if char.lower() in mapping:
            if char.isupper():
                result.append(mapping[char.lower()].upper())
            else:
                result.append(mapping[char.lower()])
        else:
            result.append(char)
    return ''.join(result)

decoded = decode(ciphertext, mapping)
print("\n\nDecoded text:")
print(decoded)
