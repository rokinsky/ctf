#include <stdio.h>
#include <stdlib.h>

// gcc -fno-stack-protector bof_simple.c -o bof_simple

void win() {
    system("/bin/sh");
}

int main() {
    char buf[0x20];
    scanf("%s", buf);
    return 0;
}
