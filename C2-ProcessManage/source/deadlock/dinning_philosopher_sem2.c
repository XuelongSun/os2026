#include<stdio.h>
#include<pthread.h>
#include<semaphore.h>

#define N 5
sem_t chopstick[N];

void *philosopher(void *id)
{
    int phil_id = *((int *)id);
    int right = phil_id;
    int left = (phil_id + 1) % N;
    while (1)
    {
        if(phil_id % 2 == 0){
            sem_wait(&chopstick[right]);
            printf(" %d got %d\n", phil_id, right);
            sem_wait(&chopstick[left]);
            printf(" %d got %d\n", phil_id, left);
        }
        else{
            sem_wait(&chopstick[left]);
            printf(" %d got %d\n", phil_id, left);
            sem_wait(&chopstick[right]);
            printf(" %d got %d\n", phil_id, right);
        }
        printf("Philosopher %d is eating\n", phil_id);
        sem_post(&chopstick[right]);
        sem_post(&chopstick[left]);
    }
}

int main()
{
    pthread_t phil[N];
    int phil_id[N];
    for (int i = 0; i < N; i++) {
        sem_init(&chopstick[i], 0, 1);
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
