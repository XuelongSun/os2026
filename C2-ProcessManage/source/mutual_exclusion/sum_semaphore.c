#include<stdio.h>
#include<pthread.h>
#include<semaphore.h>

#define N 1000000
long sum = 0;

sem_t mutex;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        sem_wait(&mutex);
        sum ++;
        sem_post(&mutex);
    }
}

int main(){
    pthread_t tA, tB;
    sem_init(&mutex, 0, 1);
    pthread_create(&tA, NULL, Tsum, &sum);
    pthread_create(&tB, NULL, Tsum, &sum);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
