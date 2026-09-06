#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int global = 100;
int *heap;

void *worker(void* arg)
{
    int local = 0;

    printf("Thread:\n");
    printf("  &global = %p\n", (void *)&global);
    printf("  heap    = %p\n", (void *)heap);
    printf("  &local  = %p\n", (void *)&local);
    return NULL;
}

int main(void)
{
    pthread_t t1, t2;
    heap = malloc(sizeof(int));
    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    free(heap);
    return 0;
}
