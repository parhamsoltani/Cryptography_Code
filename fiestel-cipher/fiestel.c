#include "feistel.h"
#include <time.h>

static uint64_t rol64(uint64_t x, int k) {
    return (x << k) | (x >> (64 - k));
}

static uint64_t round_function(uint64_t input, uint64_t subkey) {
    uint64_t x = rol64(input, 7);
    x ^= subkey;
    x = rol64(x, 13);
    x *= 0x7FEF7FEF7FEF7FEF;  // multiplication for better diffusion
    x = rol64(x, 17);
    return x;
}

static void add_padding(uint8_t* data, size_t* len) {
    size_t pad_len = BLOCK_SIZE - (*len % BLOCK_SIZE);
    memset(data + *len, (uint8_t)pad_len, pad_len);
    *len += pad_len;
}

int initialize_key(FeistelKey* key_schedule, const uint8_t* key) {
    if (!key_schedule || !key)
        return ERROR_INVALID_INPUT;

    // Copy key
    memcpy(&key_schedule->key, key, KEY_SIZE);
    
    // Check for weak keys (all zeros or all ones)
    if (key_schedule->key == 0 || key_schedule->key == UINT64_MAX)
        return ERROR_INVALID_KEY;

    // Initialize words
    for (int i = 0; i < 4; i++) {
        key_schedule->words[i] = (uint16_t)(key_schedule->key >> (48 - i*16));
    }

    generate_subkeys(key_schedule);
    return SUCCESS;
}

void generate_subkeys(FeistelKey* key_schedule) {
    uint64_t prev_key = key_schedule->key;
    
    for (int i = 0; i < ROUNDS; i++) {
        // Complex key schedule with multiple rotations and XOR operations
        uint64_t temp = rol64(prev_key, 11);
        temp ^= rol64(prev_key, 23);
        temp += i * 0x123456789ABCDEF0;  // Add round constant
        key_schedule->subkeys[i] = temp;
        prev_key = temp;
    }
}

void secure_zero(void* ptr, size_t size) {
    volatile uint8_t* p = (volatile uint8_t*)ptr;
    while (size--) {
        *p++ = 0;
    }
}

int encrypt_block(const FeistelKey* key_schedule, Block* block) {
    if (!key_schedule || !block)
        return ERROR_INVALID_INPUT;

    uint64_t left = block->left;
    uint64_t right = block->right;

    for (int i = 0; i < ROUNDS; i++) {
        uint64_t temp = right;
        right = left ^ round_function(right, key_schedule->subkeys[i]);
        left = temp;
    }

    block->left = right;  // Final swap
    block->right = left;
    return SUCCESS;
}

int decrypt_block(const FeistelKey* key_schedule, Block* block) {
    if (!key_schedule || !block)
        return ERROR_INVALID_INPUT;

    uint64_t left = block->left;
    uint64_t right = block->right;

    for (int i = ROUNDS - 1; i >= 0; i--) {
        uint64_t temp = right;
        right = left ^ round_function(right, key_schedule->subkeys[i]);
        left = temp;
    }

    block->left = right;
    block->right = left;
    return SUCCESS;
}

int encrypt_cbc(const FeistelKey* key_schedule, uint8_t* iv, 
                uint8_t* data, size_t len, uint8_t* out) {
    if (!key_schedule || !iv || !data || !out)
        return ERROR_INVALID_INPUT;

    // Add padding
    size_t padded_len = len;
    add_padding(data, &padded_len);

    Block prev_block;
    memcpy(&prev_block, iv, BLOCK_SIZE);

    for (size_t i = 0; i < padded_len; i += BLOCK_SIZE) {
        Block current_block;
        memcpy(&current_block, data + i, BLOCK_SIZE);

        // XOR with previous ciphertext or IV
        current_block.left ^= prev_block.left;
        current_block.right ^= prev_block.right;

        // Encrypt block
        encrypt_block(key_schedule, &current_block);

        // Store result
        memcpy(out + i, &current_block, BLOCK_SIZE);
        prev_block = current_block;
    }

    return SUCCESS;
}

int decrypt_cbc(const FeistelKey* key_schedule, uint8_t* iv, 
                uint8_t* data, size_t len, uint8_t* out) {
    if (!key_schedule || !iv || !data || !out || len % BLOCK_SIZE != 0)
        return ERROR_INVALID_INPUT;

    Block prev_block;
    memcpy(&prev_block, iv, BLOCK_SIZE);

    for (size_t i = 0; i < len; i += BLOCK_SIZE) {
        Block current_block;
        Block cipher_block;
        memcpy(&current_block, data + i, BLOCK_SIZE);
        cipher_block = current_block;

        // Decrypt block
        decrypt_block(key_schedule, &current_block);

        // XOR with previous ciphertext or IV
        current_block.left ^= prev_block.left;
        current_block.right ^= prev_block.right;

        // Store result
        memcpy(out + i, &current_block, BLOCK_SIZE);
        prev_block = cipher_block;
    }

    // Remove padding
    uint8_t pad_len = out[len - 1];
    if (pad_len <= BLOCK_SIZE) {
        len -= pad_len;
    }

    return SUCCESS;
}
