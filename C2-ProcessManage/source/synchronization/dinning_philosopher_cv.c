#include<stdio.h>
#include<pthread.h>
#include<stdbool.h>

#define N 5

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cv = PTHREAD_COND_INITIALIZER;

bool available[5] = {true, true, true, true, true}; 

void *philosopher(void *id)
{
    int phil_id = *((int *)id);
    int right = phil_id;
    int left = (phil_id + 1) % N;
    
    while (1)
    {
        pthread_mutex_lock(&lock);
        while(!(available[left] && available[right])){
            pthread_cond_wait(&cv, &lock);
        }
        available[left] = available[right] = false;
        printf(" %d got %d\n", phil_id, left);
        printf(" %d got %d\n", phil_id, right);
        pthread_mutex_unlock(&lock);
        printf("Philosopher %d is eating...\n", phil_id);
        pthread_mutex_lock(&lock);
        available[left] = available[right] = true;
        pthread_mutex_unlock(&lock);
        pthread_cond_broadcast(&cv);
    }
}

int main()
{   
    pthread_t phil[N];

    int phil_id[N];

    for (int i = 0; i < N; i++) {
        phil_id[i] = i;
    }
    for (int i = 0; i < N; i++) {
        pthread_create(&phil[i], NULL, philosopher, &phil_id[i]);
    }
    for (int i = 0; i < N; i++) {
        pthread_join(phil[i], NULL);
    }
    return 0;
}
