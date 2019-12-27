#include <stdio.h>
#include <unistd.h>

int main(void) {
    char buf[0x10] = { 0 };

    printf("printf: %p\n", &printf);

    read(0, buf, 0x100);

    return 0;
}
