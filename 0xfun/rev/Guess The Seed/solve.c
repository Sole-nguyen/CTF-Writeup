#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);
    
    // Generate and output 5 numbers modulo 1000
    for (int i = 0; i < 5; i++) {
        printf("%d", rand() % 1000);
        if (i < 4) printf(" ");
    }
    printf("\n");
    
    return 0;
}
