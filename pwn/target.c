#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>


struct object {
    char type;
    int size;
    char data[0x100];
};

enum obj_type {
    READ_T,
    WRITE_T,
    APPEND_T,
    END_T,
};

void readn(char *ptr, size_t size) {
    size_t count = 0;

    while (count < size) {
        ssize_t x = read(STDIN_FILENO, ptr + count, size - count);
        if (x <= 0) {
            puts("Error: read failed!");
            _exit(1);
        }
        count += x;
    }
}

void get_obj(void *ptr) {
    puts("Send encrypted object:");
    readn(ptr, sizeof(struct object));

    // decrypting ...
    memfrob(ptr, sizeof(struct object));
}

int main(void) {
    struct object obj = { 0 };
    char buf[0x100] = { 0 };

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    puts("Welcome to encrypted RPC service!");

    while (1) {
        get_obj(&obj);

        switch (obj.type) {
            case READ_T:
                if (obj.size > sizeof(buf)) {
                    puts("Overflow detected!");
                    return 1;
                }
                memcpy(buf, obj.data, obj.size);
                break;
            case WRITE_T:
                printf("data: %s\n", buf);
                break;
            case APPEND_T:
                if (obj.size > sizeof(buf)) {
                    puts("Overflow detected!");
                    return 1;
                }
                memcpy(buf + strlen(buf), obj.data, obj.size);
                break;
            case END_T:
                return 0;
            default:
                puts("Invalid object!");
                break;
        }
    }
}
