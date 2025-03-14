#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *fptr = fopen("flag.txt", "r");

    if (fptr == NULL)
    {
        printf("Not able to open the file.");
    }

    char flag[100];
    fgets(flag, 100, fptr);

    printf("The flag is: %s", flag);
}