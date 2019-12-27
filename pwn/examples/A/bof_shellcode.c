#include <stdio.h>

// gcc -fno-stack-protector -z execstack bof_shellcode.c -o bof_shellcode

int main() {
    char buf[0x20];
    scanf("%s", buf);
    return 0;
}
