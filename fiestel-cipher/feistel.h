#ifndef FEISTEL_H
#define FEISTEL_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 16
#define BLOCK_SIZE 16  // 128 bits
#define KEY_SIZE 8     // 64 bits
#define SUCCESS 0
#define ERROR_INVALID_KEY 1
#define ERROR_INVALID_INPUT 2

typedef struct {
    uint64_t key;
    uint16_t words[4];
    uint64_t subkeys[ROUNDS];
} FeistelKey;

typedef struct {
    uint64_t left;
    uint64_t right;
} Block;

int initialize_key(FeistelKey* key_schedule, const uint8_t* key);
void secure_zero(void* ptr, size_t size);
void generate_subkeys(FeistelKey* key_schedule);

// Core cipher functions
int encrypt_block(const FeistelKey* key_schedule, Block* block);
int decrypt_block(const FeistelKey* key_schedule, Block* block);

// CBC mode functions
int encrypt_cbc(const FeistelKey* key_schedule, uint8_t* iv, 
                uint8_t* data, size_t len, uint8_t* out);
int decrypt_cbc(const FeistelKey* key_schedule, uint8_t* iv, 
                uint8_t* data, size_t len, uint8_t* out);

#endif
