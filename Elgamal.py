import random
from math import pow

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

# Generating large prime number
def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

# Asymmetric encryption
def encrypt(msg, q, h, g):
    ct = []
    k = gen_key(q)
    s = power(h, k, q)
    p = power(g, k, q)
    
    for i in range(0, len(msg)):
        ct.append(msg[i])
    
    print("g^k used: ", p)
    print("g^ak used: ", s)
    
    for i in range(0, len(ct)):
        ct[i] = s * ord(ct[i])
    
    return ct, p

# Asymmetric decryption
def decrypt(ct, p, key, q):
    pt = []
    h = power(p, key, q)
    
    for i in range(0, len(ct)):
        pt.append(chr(int(ct[i]/h)))
    
    return pt

def main():
    msg = input("Enter message: ")
    q = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, q)
    
    key = gen_key(q)
    h = power(g, key, q)
    
    print("g used: ", g)
    print("g^a used: ", h)
    
    ct, p = encrypt(msg, q, h, g)
    print("Encrypted message:", ct)
    
    pt = decrypt(ct, p, key, q)
    d_msg = ''.join(pt)
    print("Decrypted message:", d_msg)

if __name__ == '__main__':
    main()