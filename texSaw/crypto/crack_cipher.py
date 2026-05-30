#!/usr/bin/env python3
import string
from collections import Counter

ciphertext = """Azza wfahv ztu. N rnvy, bndfah na zbfaztv vztak, n vztak ndfa uz n dcnqza zw n uzlvfa, icfuv nmztu. Nthtvutv, rgz gnv gnk n mnk afhgu, vfuv ty mcfadfah nak ytwmcfak. Zg rgnu rnv ugnu rzwk (fv gfv ugzthgu) ugnu wna ugwzthg bp mwnfa ncc afhgu, ugnu fkfzufl rzwk ugnu, gnwk nv F'k uwp uz yta fu kzra, rnv ncrnpv etvu na falg zw urz ztu zi bp hwnvy - izrc zw iztc zw Szr zw Szpnc? - n rzwk rgflg, mp nvvzlfnufza, mwzthgu fauz ycnp na falzahwtztv bnvv nak bnhbn zi aztav, fkfzbv, vczhnav nak vnpfahv, n lzaitvfah, nbzwygztv ztuyztwfah rgflg F vzthgu fa snfa uz lzauwzc zw utwa zii mtu rgflg rztak nwztak bp bfak n rgfwcrfak zi n lzwk, n rgfycnvg zi n lzwk, n lzwk ugnu rztck vycfu nhnfa nak nhnfa, rztck dafu nhnfa nak nhnfa, zi rzwkv rfugztu lzbbtaflnufza zw nap yzvvfmfcfup zi lzbmfanufza, rzwkv rfugztu ywzanalfnufza, vfhafiflnufza zw uwnavlwfyufza mtu ztu zi rgflg, azurfugvunakfah, rnv mwzthgu izwug n ictq, n lzaufatztv, lzbynlu nak ctlfk iczr: na fautfufza, n snlfccnufah iwfvvza zi fcctbfanufza nv fi lnthgu fa n icnvg zi cfhguafah zw fa n bfvu nmwtyucp wfvfah uz tavgwztk na zmsfztv vfha - mtu n vfha, ncnv, ugnu rztck cnvu na favunau zacp uz snafvg izw hzzk."""

# This looks like a simple substitution cipher
# Key patterns: "ugnu" appears often (likely "that")
# Single letter "N" and "F" (likely "A" and "I")
# "nak" (likely "and")

# Let me try a more systematic approach
# Based on common words and patterns:

mapping = {
    'u': 't',  # from "ugnu" = "that"
    'g': 'h',
    'n': 'a',  
    't': 'n',  # "ugnu" = "that" gives us u=t, g=h, a=t (but a is taken), so t must map back
    'k': 'd',  # from "nak" = "and"
    'z': 'o',  # "ztu" = "out", "zw" = "or"
    'w': 'r',
    'f': 'i',  # single "F" = "I"
    'v': 's',  # "rnv" = "was", "fv" = "is"
    'r': 'w',  
    'y': 'p',  # "ty" = "up"
    'm': 'b',  # "mtu" = "but", "mp" = "by"
    'a': 'n',  # "na" = "an"
    'c': 'l',  # "ncc" = "all"
    'i': 'f',  # "zi" = "of", "izw" = "for"
    'h': 'g',  # "afhgu" = "night"
    'd': 'k',  # "ndfa" = "akin"
    'l': 'c',  # "lzauwzc" = "control"
    's': 'v',  # "snfa" = "vain"
    'q': 'z',  # "dcnqza" = "klazon"
    'p': 'y',  # "ncrnpv" = "always"
    'e': 'j',  # "etvu" = "just"
    'b': 'm',  # "bp" = "my", "nbztu" = "about"
    'x': 'x',
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
print("\n" + "="*80 + "\n")

# Let's check for remaining issues
words = decoded.split()
print("Words that still look wrong:")
for word in words[:50]:
    if 'n' in word.lower() and word.lower().count('n') > 2:
        print(word)
