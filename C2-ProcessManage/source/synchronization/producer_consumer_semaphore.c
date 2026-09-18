#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#include<stdlib.h>
#include<semaphore.h>

int limit;
sem_t mutex, empty, full;

void* producer(void *args)
{
    while(1)
    {
        sem_wait(&empty);
        sem_wait(&mutex);
        printf("{");
        sem_post(&mutex);
        sem_post(&full);
    }
}

void* consumer(void *args)
{
    while(1)
    {
        sem_wait(&full);
        sem_wait(&mutex);
        printf("}");
        sem_post(&mutex);
        sem_post(&empty);
    }
}

int main(int argc, char *argv[])
{   
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <num_producers> <num_consumers> <buffer_size>\n", argv[0]);
        return 1;
    }
    limit = atoi(argv[3]);
    sem_init(&mutex, 0, 1);
    sem_init(&empty, 0, limit);
    sem_init(&full, 0, 0);
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
