#include <stdatomic.h>
#include<stdio.h>
#include<stdbool.h>
#include<pthread.h>

#define N 1000000
long sum = 0;

atomic_bool locked = ATOMIC_VAR_INIT(false);

void lock(void)
{
    while (atomic_exchange_explicit(
               &locked,
               true,
               memory_order_acquire));
}

void unlock(void)
{
    atomic_store_explicit(
        &locked,
        false,
        memory_order_release);
}

void *Tsum(void *arg) {

    for (int k = 0; k < N; k++){
       lock();
       sum ++;
       unlock();
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
