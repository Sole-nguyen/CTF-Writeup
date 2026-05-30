#include <stdio.h>
#include <stdint.h>
#include <string.h>

uint8_t SBOX[256];
uint8_t RCON[10] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36};
uint8_t MIX_MATRIX[4][4] = {
    {0x02, 0x03, 0x01, 0x01},
    {0x01, 0x02, 0x03, 0x01},
    {0x01, 0x01, 0x02, 0x03},
    {0x03, 0x01, 0x01, 0x02}
};

uint8_t gf_mult(uint8_t a, uint8_t b) {
    uint8_t result = 0;
    for (int i = 0; i < 8; i++) {
        if (b & 1) result ^= a;
        uint8_t hi_bit = a & 0x80;
        a <<= 1;
        if (hi_bit) a ^= 0x1B;
        b >>= 1;
    }
    return result;
}

uint8_t gf_pow(uint8_t base, uint8_t exp) {
    if (exp == 0) return 1;
    uint8_t result = 1;
    while (exp > 0) {
        if (exp & 1) result = gf_mult(result, base);
        base = gf_mult(base, base);
        exp >>= 1;
    }
    return result;
}

void init_sbox() {
    for (int x = 0; x < 256; x++) {
        uint8_t val = gf_pow(x, 23);
        val ^= 0x63;
        SBOX[x] = val;
    }
}

void key_expansion(const uint8_t* key, uint8_t round_keys[5][16]) {
    uint8_t words[20][4];
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) words[i][j] = key[4*i + j];
    }
    
    for (int i = 4; i < 20; i++) {
        uint8_t temp[4];
        for(int j = 0; j < 4; j++) temp[j] = words[i-1][j];
        
        if (i % 4 == 0) {
            uint8_t t = temp[0];
            temp[0] = SBOX[temp[1]] ^ RCON[(i/4)-1];
            temp[1] = SBOX[temp[2]];
            temp[2] = SBOX[temp[3]];
            temp[3] = SBOX[t];
        }
        for(int j = 0; j < 4; j++) words[i][j] = words[i-4][j] ^ temp[j];
    }
    
    for (int r = 0; r < 5; r++) {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) round_keys[r][4*i + j] = words[r*4 + i][j];
        }
    }
}

void encrypt_block(const uint8_t* pt, const uint8_t round_keys[5][16], uint8_t* ct) {
    uint8_t state[4][4];
    for (int i = 0; i < 16; i++) state[i % 4][i / 4] = pt[i];

    // Initial AddRoundKey
    for (int c = 0; c < 4; c++) {
        for (int r = 0; r < 4; r++) state[r][c] ^= round_keys[0][r + 4*c];
    }

    for (int r_idx = 1; r_idx < 4; r_idx++) {
        // SubBytes
        for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) state[r][c] = SBOX[state[r][c]];

        // ShiftRows
        uint8_t temp[4][4];
        for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) temp[r][c] = state[r][(c + r) % 4];
        for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) state[r][c] = temp[r][c];

        // MixColumns
        for(int c = 0; c < 4; c++) {
            uint8_t col[4];
            for(int r = 0; r < 4; r++) col[r] = state[r][c];
            for(int r = 0; r < 4; r++) {
                state[r][c] = gf_mult(MIX_MATRIX[r][0], col[0]) ^
                              gf_mult(MIX_MATRIX[r][1], col[1]) ^
                              gf_mult(MIX_MATRIX[r][2], col[2]) ^
                              gf_mult(MIX_MATRIX[r][3], col[3]);
            }
        }

        // AddRoundKey
        for (int c = 0; c < 4; c++) {
            for (int r = 0; r < 4; r++) state[r][c] ^= round_keys[r_idx][r + 4*c];
        }
    }

    // Final Round
    for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) state[r][c] = SBOX[state[r][c]];

    uint8_t temp2[4][4];
    for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) temp2[r][c] = state[r][(c + r) % 4];
    for(int r = 0; r < 4; r++) for(int c = 0; c < 4; c++) state[r][c] = temp2[r][c];

    for (int c = 0; c < 4; c++) {
        for (int r = 0; r < 4; r++) state[r][c] ^= round_keys[4][r + 4*c];
    }

    // State to Bytes
    for (int c = 0; c < 4; c++) {
        for (int r = 0; r < 4; r++) ct[r + 4*c] = state[r][c];
    }
}

int main() {
    init_sbox();
    
    // Known pair from output.txt
    uint8_t pt[16] = {0x37, 0x6f, 0x73, 0x33, 0x4d, 0xc9, 0xdb, 0x2a, 0x4d, 0x20, 0x73, 0x4c, 0x07, 0x83, 0xac, 0x69};
    uint8_t expected_ct[16] = {0x90, 0x70, 0xf8, 0x1f, 0x4d, 0xe7, 0x89, 0x66, 0x38, 0x20, 0xe8, 0x92, 0x49, 0x24, 0x73, 0x2b};
    uint8_t key[16] = {0x26, 0xab, 0x77, 0xca, 0xdc, 0xca, 0x0e, 0xd4, 0x1b, 0x03, 0xc8, 0xf2, 0xe5, 0x00, 0x00, 0x00};
    
    uint8_t ct[16];
    uint8_t round_keys[5][16];

    printf("[*] Starting fast C brute-force...\n");

    for (uint32_t i = 0; i <= 0xFFFFFF; i++) {
        key[13] = (i >> 16) & 0xFF;
        key[14] = (i >> 8) & 0xFF;
        key[15] = i & 0xFF;

        key_expansion(key, round_keys);
        encrypt_block(pt, round_keys, ct);

        if (memcmp(ct, expected_ct, 16) == 0) {
            printf("[+] KEY FOUND: ");
            for(int j = 0; j < 16; j++) printf("%02x", key[j]);
            printf("\n");
            return 0;
        }
    }
    
    printf("[-] Key not found.\n");
    return 1;
}