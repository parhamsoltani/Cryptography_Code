# Feistel Cipher Implementation

A secure implementation of a Feistel network cipher in C, featuring CBC mode encryption.

## Features

- 16-round Feistel network structure
- 128-bit block size with 64-bit key
- CBC (Cipher Block Chaining) mode of operation
- PKCS7-style padding
- Enhanced round function with rotations and diffusion
- Secure key scheduling with round constants
- Memory-safe implementation with proper cleanup
- Input validation and error handling

## Technical Details

### Security Features

- Complex round function incorporating:
  - Bit rotations
  - XOR operations
  - Multiplication-based diffusion
- Secure key schedule with:
  - Multiple rotations
  - Round-specific constants
  - Weak key detection
- Secure memory handling:
  - Volatile memory zeroing
  - Protected key storage
  - Buffer overflow prevention

### Implementation Structure

feistel.h - Main header file with interface definitions
feistel.c - Core implementation of the cipher
main.c - Example usage and testing

### Key Components

- `FeistelKey`: Structure for key schedule storage
- `Block`: Structure for block operations
- Core functions:
  - `initialize_key()`: Key schedule initialization
  - `encrypt_block()`: Single block encryption
  - `decrypt_block()`: Single block decryption
  - `encrypt_cbc()`: CBC mode encryption
  - `decrypt_cbc()`: CBC mode decryption

## Usage

```c

#include "feistel.h"

// Initialize key schedule
FeistelKey key_schedule;
uint8_t key[KEY_SIZE] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF};
initialize_key(&key_schedule, key);

// Prepare data
uint8_t iv[BLOCK_SIZE] = {0}; // Initialization Vector
uint8_t plaintext[] = "Hello, World!";
size_t data_len = strlen((char*)plaintext);

// Encrypt data
size_t padded_length = ((data_len / BLOCK_SIZE) + 1) * BLOCK_SIZE;
uint8_t* ciphertext = malloc(padded_length);
encrypt_cbc(&key_schedule, iv, plaintext, data_len, ciphertext);

// Decrypt data
uint8_t* decrypted = malloc(padded_length);
decrypt_cbc(&key_schedule, iv, ciphertext, padded_length, decrypted);

// Clean up
free(ciphertext);
free(decrypted);
```

## Security Considerations

This implementation is for **educational purposes only** and has not undergone formal cryptographic review.

### Important Notes:
- The key size (**64 bits**) is insufficient for modern security standards.
- For production systems, use established cryptographic libraries like [OpenSSL](https://www.openssl.org/).

---

## Building and Testing

To compile and run the implementation:

### Compile:
```bash
gcc -o feistel main.c feistel.c -Wall -Wextra -O2
```

### Run:
```bash
./feistel
```
## Dependencies
- Standard C library
- C99 compatible compiler
---

>Disclaimer:
>This implementation is intended for educational purposes only.
>Do not use it in production systems without thorough security review and modifications.
