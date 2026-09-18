#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#include<stdlib.h>

int limit, count = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cv = PTHREAD_COND_INITIALIZER;

void* producer(void *args)
{
    while(1)
    {
        pthread_mutex_lock(&lock);
        while(count >= limit){
            pthread_cond_wait(&cv, &lock);
        }
        count++;
        printf("{");
        pthread_cond_broadcast(&cv);
        pthread_mutex_unlock(&lock);
    }
}

void* consumer(void *args)
{
    while(1)
    {
        pthread_mutex_lock(&lock);
        while(count <= 0){
            pthread_cond_wait(&cv, &lock);
        }
        count--;
        printf("}");
        pthread_cond_broadcast(&cv);
        pthread_mutex_unlock(&lock);
    }
}

int main(int argc, char *argv[])
{   
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <num_producers> <num_consumers> <buffer_size>\n", argv[0]);
        return 1;
    }
    limit = atoi(argv[3]);
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
