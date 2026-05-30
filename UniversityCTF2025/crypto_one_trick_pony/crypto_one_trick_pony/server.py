import hashlib, json
from Crypto.Util.number import getPrime, isPrime
from random import randint

STARSCROLL = open("flag.txt").read()

assert len(STARSCROLL.strip("HTB{}")) == 79

class TinselRNG:
    def __init__(self, bits):
        self.holly_prime = getPrime(bits)
        self.sleigh_seed = randint(1, self.holly_prime)

    def sparkle_bit(self):
        if self.sleigh_seed == 0:
            self.sleigh_seed += 1
        while True:
            shimmer = pow(self.sleigh_seed, (self.holly_prime-1)//2, self.holly_prime)
            yield int(shimmer == 1)
            self.sleigh_seed = (self.sleigh_seed + 1) % self.holly_prime
            if self.sleigh_seed == 0:
                self.sleigh_seed += 1

    def gather_sparkles(self, l):
        bits = ''
        for i, b in enumerate(self.sparkle_bit()):
            if i == l: break
            bits += str(b)
        return int(bits, 2)

assert isPrime(FROST_PRIME := 0x1a66804d885939d7acf3a4b413c9a24547b876e706913adec9684cc4a63ab0dfd2e0fd79f683de06ad17774815dfc8375370eb3d0fb5dce0019bd0632e7663a41)

def frostscribe_signature(msg):
    blizzard = hashlib.sha512(msg.encode()).digest()
    snowmark = int.from_bytes(blizzard, "big") % FROST_PRIME
    lantern_key = frostrng.gather_sparkles(500)
    etch = pow(snowmark, lantern_key, FROST_PRIME)
    return {"signature": str(etch)}

frostrng = TinselRNG(34)

print(f'{frostrng.holly_prime = }')

LIMIT = 2_000

print("Welcome to the Snowglobe Cipher Booth!\n")
while True:
    if LIMIT <= 0:
        print("The lantern dims for today...")
        break

    print("1) Etch Message Rune")
    print("2) Request Wrapped Starshard")
    print("3) Leave Booth")

    choice = input("> ").strip()

    if choice == "1":
        msg = input("Whisper your message: ")
        print(json.dumps(frostscribe_signature(msg)))
        LIMIT -= 1

    elif choice == "2":
        snow_otp = frostrng.gather_sparkles(len(STARSCROLL)*8)
        user_otp = int(input("Reveal my snow-otp (in bits): "), 2)
        if user_otp == snow_otp:
            print(json.dumps({"starshard": STARSCROLL}))
        else:
            print(json.dumps({"starshard": "HTB{fake_flag_for_testing}"}))
        break

    elif choice == "3":
        print('May your lantern stay warm. Farewell...')
        break

    else:
        print("That choice jingled wrong.")
