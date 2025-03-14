#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

int rizz_multiplier = 2;

size_t rizz_formula(char* rizz) {
    size_t rating;
    for (int i = 0; rizz[i] != '\0'; i++) {
        rating += rizz[i] * rizz_multiplier;
    }
    return rating;
}

void win() {
    printf("You may be a skibidi rizzler after all...\n");
    char *args[] = {"/bin/sh", NULL};
    execve(args[0], args, NULL);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    char rizz[100];
    printf("Give me your best rizz: ");
    fgets(rizz, 0x100, stdin);
    rizz[strcspn(rizz, "\n")] = 0;
    printf("Here is your skibidi rizz rating: %zu\n", rizz_formula(rizz));

    printf("Now give me one final sigma baby gronk rizz: ");
    fgets(rizz, 0x100, stdin);

    printf("No gyatt for you lil bro\n");
    return 0;
}