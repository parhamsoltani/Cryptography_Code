import math
import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_number():
    while True:
        n = random.randrange(100, 1000)
        if is_prime(n):
            return n

def generate_keys():
    # Generate two prime numbers
    p = generate_prime_number()
    q = generate_prime_number()
    while p == q:
        q = generate_prime_number()
    
    # Calculate n and phi
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Generate public key e
    e = 65537  # Common value for e
    
    # Generate private key d
    d = pow(e, -1, phi)
    
    return ((e, n), (d, n))

def encrypt(message, public_key):
    e, n = public_key
    encrypted = []
    for char in message:
        # Convert character to number and encrypt
        m = ord(char)
        c = pow(m, e, n)
        encrypted.append(str(c))
    return ','.join(encrypted)

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted = ''
    # Split the encrypted message into numbers
    numbers = encrypted_message.split(',')
    for c in numbers:
        # Decrypt each number and convert back to character
        c = int(c)
        m = pow(c, d, n)
        decrypted += chr(m)
    return decrypted

def main():
    # Generate keys
    public_key, private_key = generate_keys()
    print("Public Key (e,n):", public_key)
    print("Private Key (d,n):", private_key)
    
    # Read message from file
    try:
        with open('input.txt', 'r', encoding='utf-8') as file:
            message = file.read()
    except FileNotFoundError:
        message = "Hello, RSA!"  # Default message if file not found
    
    print("\nOriginal Message:", message)
    
    # Encrypt
    encrypted_message = encrypt(message, public_key)
    print("\nEncrypted Message:", encrypted_message)
    
    # Decrypt
    decrypted_message = decrypt(encrypted_message, private_key)
    print("\nDecrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()