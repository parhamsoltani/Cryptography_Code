def calculate_keys(p, q, r):
    m = p * q
    n = p * q * (p - 1) * (q - 1)
    
    # Calculate α(n)
    alpha_n = ((p - 1) * (q - 1) * (p - 2**r) * (q - 2**r)) // 2**r
    
    # Find e (coprime with α(n))
    def find_e(alpha_n):
        for e in range(2, alpha_n):
            if gcd(e, alpha_n) == 1:
                return e
    
    e = find_e(alpha_n)
    
    # Calculate d (multiplicative inverse of e mod α(n))
    d = mod_inverse(e, alpha_n)
    
    return (e, m), (d, m)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi

def encrypt(message, public_key):
    e, m = public_key
    encrypted = []
    for char in message:
        encrypted_char = pow(ord(char), e, m)
        encrypted.append(str(encrypted_char))
    return ','.join(encrypted)

if __name__ == "__main__":
    with open("input.txt", "r", encoding='utf-8') as f:
        message = f.read()
    
    p = 17
    q = 11
    r = 3
    
    public_key, private_key = calculate_keys(p, q, r)
    encrypted_text = encrypt(message, public_key)
    
    with open("encrypted.txt", "w", encoding='utf-8') as f:
        f.write(encrypted_text)