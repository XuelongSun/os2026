#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("PID = %d\n", getpid());

    while (1) {
        printf("CPU working...\n");

        for (volatile long i = 0; i < 5000000000; ++i) {
        }

        printf("waiting...\n");
        sleep(3);
    }
}
