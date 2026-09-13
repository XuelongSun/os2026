#include<stdio.h>
#include<stdbool.h>
#include<pthread.h>

#define N 1000000
long sum = 0;
bool flag[2];
int turn = 0;

void *Tsum(void *arg) {
    int i = *(int *)arg;
    int j = 1 - i;
    for (int k = 0; k < N; k++){
        flag[i] = 1; //举旗
        turn = j; //贴条：让出优先权
        while(flag[j] && turn == j);
        sum ++;
        flag[i] = 0; //放下旗帜
    }
}

int main(){
    pthread_t tA, tB;
    int flagA = 0;
    int flagB = 1;
    pthread_create(&tA, NULL, Tsum, &flagA);
    pthread_create(&tB, NULL, Tsum, &flagB);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
