// gcc global_buf.c -o global_buf

#include <stdio.h>
#include <stdlib.h>

#define BUF_SIZE 0x10

int buf[BUF_SIZE];

int main() {
    int offset = 0,
        num = 0,
        i = 0;

    system("echo \"Witaj!\"");
    for (i = 0; i < BUF_SIZE; ++i) {
        scanf("%d", &offset);
        scanf("%d", &num);
        buf[offset] = num;
    }

    puts((const char *)buf);

    return 0;
}
