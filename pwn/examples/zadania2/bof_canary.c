#include <stdio.h>

// 1. gcc -no-pie -z execstack bof_canary.c -o bof_canary_execstack
// 2. turn on asrl
// 3. gcc bof_canary.c -o bof_canary

int main() {
    unsigned int count = 1;
    char buf[0x30] = {0};

    do {
        fscanf(stdin, "%u", &count);
        fgetc(stdin);
        fread(buf, 1, count, stdin);
        fprintf(stdout, "%s\n", buf);
    } while (count > 0);

    return 0;
}
