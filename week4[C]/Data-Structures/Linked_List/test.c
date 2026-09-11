#include <stdio.h>
#include <stdlib.h>

int global = 1;

int main(void) {
    int local = 2;
    int *heap = malloc(sizeof(int));

    printf("전역:  %p\n", (void*)&global);
    printf("힙:    %p\n", (void*)heap);
    printf("스택:  %p\n", (void*)&local);
    printf("코드:  %p\n", (void*)main);

    free(heap);
}