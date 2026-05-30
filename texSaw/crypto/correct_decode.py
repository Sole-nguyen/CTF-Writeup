ciphertext = """Azza wfahv ztu. N rnvy, bndfah na zbfaztv vztak, n vztak ndfa uz n dcnqza zw n uzlvfa, icfuv nmztu. Nthtvutv, rgz gnv gnk n mnk afhgu, vfuv ty mcfadfah nak ytwmcfak. Zg rgnu rnv ugnu rzwk (fv gfv ugzthgu) ugnu wna ugwzthg bp mwnfa ncc afhgu, ugnu fkfzufl rzwk ugnu, gnwk nv F'k uwp uz yta fu kzra, rnv ncrnpv etvu na falg zw urz ztu zi bp hwnvy - izrc zw iztc zw Szr zw Szpnc? - n rzwk rgflg, mp nvvzlfnufza, mwzthgu fauz ycnp na falzahwtztv bnvv nak bnhbn zi aztav, fkfzbv, vczhnav nak vnpfahv, n lzaitvfah, nbzwygztv ztuyztwfah rgflg F vzthgu fa snfa uz lzauwzc zw utwa zii mtu rgflg rztak nwztak bp bfak n rgfwcrfak zi n lzwk, n rgfycnvg zi n lzwk, n lzwk ugnu rztck vycfu nhnfa nak nhnfa, rztck dafu nhnfa nak nhnfa, zi rzwkv rfugztu lzbbtaflnufza zw nap yzvvfmfcfup zi lzbmfanufza, rzwkv rfugztu ywzanalfnufza, vfhafiflnufza zw uwnavlwfyufza mtu ztu zi rgflg, azurfugvunakfah, rnv mwzthgu izwug n ictq, n lzaufatztv, lzbynlu nak ctlfk iczr: na fautfufza, n snlfccnufah iwfvvza zi fcctbfanufza nv fi lnthgu fa n icnvg zi cfhguafah zw fa n bfvu nmwtyucp wfvfah uz tavgwztk na zmsfztv vfha - mtu n vfha, ncnv, ugnu rztck cnvu na favunau zacp uz snafvg izw hzzk."""

# Correct mapping - b should map to 'b' and m to 'm', or check which is which
# Looking at "bp" which should be "my" or "by"
# "bp mwnfa" = "?y ?rain" = "by brain" or "my brain"
# Both could work, but "my brain" sounds more natural
# So b->m, p->y

# Looking at "mtu" which should be "but" 
# So m->b

# Hmm, contradiction. Let me check: "nmztu" should be "about"
# a->n gives 'n', m->?, z->o, t->u, u->t
# "n?out" = "about" means ?=b, so m->b

# And "bp" should be... if m->b, then b->?
# "?y" = "my" means b->m!

mapping = {
    'a': 'n',
    'b': 'm',  # from "bp" = "my"
    'c': 'l',
    'd': 'k',
    'e': 'j',
    'f': 'i',
    'g': 'h',
    'h': 'g',
    'i': 'f',
    'k': 'd',
    'l': 'c',
    'm': 'b',  # from "mtu" = "but", "nmztu" = "about"
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
