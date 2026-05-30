#include <stdio.h>

int main() {
    long values_base = 0x6010c0;
    long puts_got = 0x601020;
    long msg_addr = 0x601068;
    
    int offset_puts = (puts_got - values_base) / 4;
    int offset_msg = (msg_addr - values_base) / 4;
    
    printf("Offset to puts@GOT: %d\n", offset_puts);
    printf("Offset to msg: %d\n", offset_msg);
    
    return 0;
}
