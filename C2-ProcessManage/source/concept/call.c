#include <stdio.h>

void B(void)
{
    int b = 20;
    printf("B: &b = %p\n", (void *)&b);
}

void A(void)
{
    int a = 10;
    printf("A: &a = %p\n", (void *)&a);
    B();
}

int main(void)
{
    int m = 0;
    printf("main: &m = %p\n", (void *)&m);
    A();
    return 0;
}
