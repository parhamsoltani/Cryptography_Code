import random

class Key:
    def __init__(self, k=None):
        if k is None:
            self.k = random.getrandbits(64)
        else:
            self.k = k
        self.set_word()

    def set_word(self):
        self.w = [
            (self.k >> 48) & 0xFFFF,
            (self.k >> 32) & 0xFFFF,
            (self.k >> 16) & 0xFFFF,
            self.k & 0xFFFF
        ]

    def get_word(self, i):
        if i > 3:
            return -1
        return self.w[i]

    def get_word_byte(self, i):
        wb0 = (self.w[i] >> 12) & 0xF
        wb1 = (self.w[i] >> 8) & 0xF
        wb2 = (self.w[i] >> 4) & 0xF
        wb3 = self.w[i] & 0xF
        return [wb0, wb1, wb2, wb3]

    def rot_word(self, i):
        v = self.get_word_byte(i)
        if not v:
            return -1
        return (v[1] << 12) | (v[2] << 8) | (v[3] << 4) | v[0]

    def generate_sub_key(self):
        rotw3 = self.rot_word(3)
        w4 = self.w[0] ^ rotw3
        w5 = self.w[1] ^ w4
        w6 = self.w[2] ^ w5
        w7 = self.w[3] ^ w6
        n_k = (w4 << 48) | (w5 << 32) | (w6 << 16) | w7
        return Key(n_k)

    def print_key(self):
        print(f"{self.w[0]:04x}{self.w[1]:04x}{self.w[2]:04x}{self.w[3]:04x}")

    def get_key(self):
        return self.k

class Feistel:
    def __init__(self, k):
        self.k = k
        self.sub_keys = []
        self.generate_sub_keys()

    def generate_sub_keys(self):
        self.sub_keys.append(self.k.generate_sub_key())
        self.sub_keys.append(self.sub_keys[0].generate_sub_key())
        self.sub_keys.append(self.sub_keys[1].generate_sub_key())
        self.sub_keys.append(self.sub_keys[2].generate_sub_key())

    def print_sub_keys(self):
        for sk in self.sub_keys:
            sk.print_key()

    def calc_feistel_round(self, r_k, l, r):
        r_k_u = r_k.get_key()
        tmp = r ^ r_k_u
        return tmp ^ l

    def encrypt(self, lpt, rpt):
        r1 = self.calc_feistel_round(self.sub_keys[0], lpt, rpt)
        r2 = self.calc_feistel_round(self.sub_keys[1], rpt, r1)
        r3 = self.calc_feistel_round(self.sub_keys[2], r1, r2)
        r4 = self.calc_feistel_round(self.sub_keys[3], r2, r3)
        return [r4, r3]

    def decrypt(self, lct, rct):
        r1 = self.calc_feistel_round(self.sub_keys[3], lct, rct)
        r2 = self.calc_feistel_round(self.sub_keys[2], rct, r1)
        r3 = self.calc_feistel_round(self.sub_keys[1], r1, r2)
        r4 = self.calc_feistel_round(self.sub_keys[0], r2, r3)
        return [r4, r3]

def main():
    print("Enter the 2 numbers you want to encrypt:")
    p1 = int(input())
    p2 = int(input())

    k = Key()
    print("The random key is:")
    k.print_key()
    
    print("The rotWord function result on the 3rd word is:")
    print(hex(k.rot_word(3)))

    f = Feistel(k)
    print("The subkeys are:")
    f.print_sub_keys()

    enc = f.encrypt(p1, p2)
    dec = f.decrypt(enc[0], enc[1])

    print("Result after encryption is:")
    print(f"{enc[0]}{enc[1]}")
    print("Result after decryption is:")
    print(f"{dec[0]} {dec[1]}")

if __name__ == "__main__":
    main()