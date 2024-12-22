from encryption import calculate_keys, encrypt
from decryption import decrypt

def main():
    # Read input text
    with open("input.txt", "r", encoding='utf-8') as f:
        message = f.read()
    
    # Parameters
    p = 17
    q = 11
    r = 3
    
    print("Step 1: Generating keys...")
    public_key, private_key = calculate_keys(p, q, r)
    print(f"Public key (e,m): {public_key}")
    print(f"Private key (d,m): {private_key}")
    
    print(f"\nStep 2: Original message from input.txt: {message}")
    
    print("\nStep 3: Encrypting...")
    encrypted_text = encrypt(message, public_key)
    print(f"Encrypted text: {encrypted_text}")
    
    # Save encrypted text
    with open("encrypted.txt", "w", encoding='utf-8') as f:
        f.write(encrypted_text)
    
    print("\nStep 4: Decrypting...")
    decrypted_text = decrypt(encrypted_text, private_key)
    print(f"Decrypted text: {decrypted_text}")
    
    # Save decrypted text
    with open("decrypted.txt", "w", encoding='utf-8') as f:
        f.write(decrypted_text)

if __name__ == "__main__":
    main()