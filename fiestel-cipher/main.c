#include <stdio.h>
#include "feistel.h"

void print_hex(const uint8_t* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", data[i]);
    }
    printf("\n");
}

int main() {
    // Test key
    uint8_t key[KEY_SIZE] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF};
    uint8_t iv[BLOCK_SIZE] = {0}; // Initialize IV with zeros
    
    // Initialize key schedule
    FeistelKey key_schedule;
    if (initialize_key(&key_schedule, key) != SUCCESS) {
        printf("Key initialization failed\n");
        return 1;
    }

    // Test data
    uint8_t plaintext[] = "Hello, World!";
    size_t data_len = strlen((char*)plaintext);
    
    // Allocate buffers for encrypted and decrypted data
    size_t padded_len = data_len + (BLOCK_SIZE - (data_len % BLOCK_SIZE));
    uint8_t* ciphertext = malloc(padded_len);
    uint8_t* decrypted = malloc(padded_len);

    // Encrypt
    printf("Original: %s\n", plaintext);
    printf("Original (hex): ");
    print_hex(plaintext, data_len);

    if (encrypt_cbc(&key_schedule, iv, plaintext, data_len, ciphertext) != SUCCESS) {
        printf("Encryption failed\n");
        return 1;
    }

    printf("Encrypted (hex): ");
    print_hex(ciphertext, padded_len);

    // Reset IV for decryption
    memset(iv, 0, BLOCK_SIZE);

    // Decrypt
    if (decrypt_cbc(&key_schedule, iv, ciphertext, padded_len, decrypted) != SUCCESS) {
        printf("Decryption failed\n");
        return 1;
    }

    printf("Decrypted: %s\n", decrypted);
    printf("Decrypted (hex): ");
    print_hex(decrypted, data_len);

    // Clean up
    secure_zero(&key_schedule, sizeof(FeistelKey));
    free(ciphertext);
    free(decrypted);

    return 0;
}
