#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int power;  // 4 bytes
    char pad[4];  // padding
    char *name;  // 8 bytes
} Player;

int main() {
    Player *p1 = malloc(sizeof(Player));
    p1->power = 0x14;
    p1->name = malloc(8);
    
    Player *p2 = malloc(sizeof(Player));
    p2->power = 0x14;
    p2->name = malloc(8);
    
    printf("p1: %p\n", p1);
    printf("p1->name: %p\n", p1->name);
    printf("p2: %p\n", p2);
    printf("p2->name: %p\n", p2->name);
    printf("Distance p1->name to p2: %ld\n", (char*)p2 - (char*)p1->name);
    
    // Test overflow
    strcpy(p1->name, "AAAAAAAABBBBBBBBCCCCCCCC");
    printf("\nAfter overflow:\n");
    printf("p2->power: 0x%x\n", p2->power);
    printf("p2->name: %p\n", p2->name);
    
    return 0;
}
