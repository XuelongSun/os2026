#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int x = 0;
int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("usage: %s number\n", argv[0]);
        return 1;
    }
    x = atoi(argv[1]);
    printf("&x  = %p\n", (void *)&x);
    while (1) {
        printf("x=%d\n",x);
        sleep(2);
    }
}
