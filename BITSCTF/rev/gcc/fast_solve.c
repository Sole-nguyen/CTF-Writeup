#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main() {
    FILE *f = fopen("ghost_compiler", "rb");
    if (!f) {
        printf("Cannot open file\n");
        return 1;
    }
    
    fseek(f, 0, SEEK_END);
    long file_size = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    uint8_t *data = malloc(file_size);
    fread(data, 1, file_size, f);
    fclose(f);
    
    printf("File size: %ld bytes\n", file_size);
    printf("Searching for flag...\n");
    
    for (long offset = 0; offset < file_size - 64; offset++) {
        // Compute FNV-1a hash skipping 64 bytes at offset
        uint64_t key = 0xCBF29CE484222325ULL;
        for (long i = 0; i < file_size; i++) {
            if (i >= offset && i < offset + 64) continue;
            key ^= data[i];
            key *= 0x100000001B3ULL;
        }
        key ^= 0xCAFEBABE00000000ULL;
        
        // Try to decrypt first 8 bytes
        uint64_t temp_key = key;
        uint8_t decrypted[8];
        for (int i = 0; i < 8; i++) {
            decrypted[i] = data[offset + i] ^ (temp_key & 0xFF);
            // Rotate right by 1
            temp_key = (temp_key >> 1) | ((temp_key & 1) << 63);
        }
        
        // Check for "BITSCTF{" signature
        if (memcmp(decrypted, "BITSCTF{", 8) == 0) {
            printf("Found at offset: 0x%lx\n", offset);
            
            // Decrypt full 64 bytes
            temp_key = key;
            uint8_t flag[65];
            for (int i = 0; i < 64; i++) {
                flag[i] = data[offset + i] ^ (temp_key & 0xFF);
                temp_key = (temp_key >> 1) | ((temp_key & 1) << 63);
            }
            flag[64] = '\0';
            
            printf("Flag: %s\n", flag);
            free(data);
            return 0;
        }
        
        if (offset % 1000 == 0) {
            printf("\rChecked %ld offsets...", offset);
            fflush(stdout);
        }
    }
    
    printf("\nFlag not found!\n");
    free(data);
    return 1;
}
