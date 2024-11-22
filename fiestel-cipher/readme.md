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
