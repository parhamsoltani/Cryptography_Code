def decrypt(encrypted_text, private_key):
    d, m = private_key
    decrypted = []
    encrypted_chars = encrypted_text.split(',')
    
    for char in encrypted_chars:
        decrypted_char = pow(int(char), d, m)
        decrypted.append(chr(decrypted_char))
    
    return ''.join(decrypted)

if __name__ == "__main__":
    with open("encrypted.txt", "r", encoding='utf-8') as f:
        encrypted_text = f.read()
    
    p = 17
    q = 11
    r = 3
    
    from encryption import calculate_keys
    public_key, private_key = calculate_keys(p, q, r)
    
    decrypted_text = decrypt(encrypted_text, private_key)
    
    with open("decrypted.txt", "w", encoding='utf-8') as f:
        f.write(decrypted_text)