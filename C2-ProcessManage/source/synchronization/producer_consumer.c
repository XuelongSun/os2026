#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#include<stdlib.h>

int n = 0;

void* producer(void *args)
{
    while(1)
    {
        printf("{");
    }
}

void* consumer(void *args)
{
    while(1)
    {
        printf("}");
    }
}

int main(int argc, char *argv[])
{   
    // argv[1]: number of producers
    // argv[2]: number of consumers
    // argv[3]: buffer size
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <num_producers> <num_consumers> <buffer_size>\n", argv[0]);
        return 1;
    }
    n = atoi(argv[3]);
    pthread_t p[atoi(argv[1])], c[atoi(argv[2])];
    for (int i = 0; i < atoi(argv[1]); i++) {
        pthread_create(&p[i], NULL, producer, NULL);
    }
    for (int i = 0; i < atoi(argv[2]); i++) {
        pthread_create(&c[i], NULL, consumer, NULL);
    }
    
    for (int i = 0; i < atoi(argv[1]); i++) {
        pthread_join(p[i], NULL);
    }
    for (int i = 0; i < atoi(argv[2]); i++) {
        pthread_join(c[i], NULL);
    }
    return 0;
}
