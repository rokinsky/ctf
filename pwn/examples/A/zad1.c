// gcc -O2 -o zad1 zad1.c
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    char buf[0x100] = { 0 };

    if (argc != 2) {
        return 1;
    }

    snprintf(buf, sizeof buf, "ls -al %s", argv[1]);

    system(buf);

    return 0;
}
