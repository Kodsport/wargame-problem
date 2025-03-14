#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include "config.h"

ssize_t (*org_read)(int, void*, size_t);

ssize_t read_hook(int fd, void* buf, size_t nbyte) {
    ssize_t ret = org_read(fd, buf, nbyte);
    if (ret > 0) {
        srand(1337);
        char* cbuf = (char*)buf;
        for (int i = ret-1; i >= 0; i--) {
            int j = rand() % (i+1);
            if (i == j) continue;
            char tmp = cbuf[i];
            cbuf[i] = cbuf[j];
            cbuf[j] = tmp;
        }
    }
    return ret;
}

__attribute__((constructor))
static void sneaky() {
    void** read_got;
    // load address of the GOT entry for read
    __asm__("leaq read@GOTPCREL(%%rip), %0" : "=r"(read_got));
    org_read = *read_got;
    *read_got = read_hook;
}


int main() {
    char flag[FLAG_LEN+1] = {0};
    srand(0);
    ssize_t ret = read(0, flag, FLAG_LEN);
    if (ret < 0) {
        perror("read");
        return 1;
    }
    if (ret != FLAG_LEN) {
        puts("för litet knäckebröd");
        return 1;
    }
    for (int i = 0; i < ITERS; i++) {
        int i = rand() % FLAG_LEN;
        int j = rand() % FLAG_LEN;
        int k = rand() % FLAG_LEN;
        if (i == j || j == k || i == k) continue;
        flag[i] ^= flag[j];
        flag[j] ^= flag[k];
        flag[k] ^= flag[i];
    }

    if (!memcmp(flag, target, FLAG_LEN)) {
        puts("mycket bra knäckebröd");
        return 0;
    }
    puts("dåligt knäckebröd");
    return 1;
}