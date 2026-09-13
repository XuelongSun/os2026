#include<stdio.h>
#include<pthread.h>

#define N 1000000
long sum = 0;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        sum++;
    }
}

int main(){
    pthread_t tA, tB;
    pthread_create(&tA, NULL, Tsum, NULL);
    pthread_create(&tB, NULL, Tsum, NULL);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
