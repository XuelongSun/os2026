#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("PID = %d\n", getpid());

    while (1) {
        printf("working...\n");
        sleep(2);
    }

    return 0;
}
