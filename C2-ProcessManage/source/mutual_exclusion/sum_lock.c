#include<stdio.h>
#include<stdbool.h>
#include<pthread.h>

#define N 1000000
long sum = 0;
int locked = false;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        while (locked); //wait
        locked = true;
        sum ++;
        locked = false;
    }
}

int main(){
    pthread_t tA, tB;
    pthread_create(&tA, NULL, Tsum, &sum);
    pthread_create(&tB, NULL, Tsum, &sum);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
