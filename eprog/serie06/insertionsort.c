//
// Created by ida on 17.11.20.
//

#include <stdio.h>
#include <stdlib.h>

void insertionSort(double* x, int n) {
    for (int i=1; i < n; i++) {
        int j = 0;
        for(;x[i]>x[j];j++);
        for(int k=i;k>j;k--) {
            double tmp = x[k];
            x[k] = x[k-1];
            x[k-1] = tmp;
        }
    }
}

int main() {
    printf("Sorts a given vector using insertion sort.\n");

    int n = 0;
    double* arr;

    printf("Please enter a value for the length of the vector: ");
    scanf("%d", &n);

    arr = malloc(n*sizeof(double));

    for(int i=0; i < n; i++) {
        printf("Please enter a value for x[%d]= ",i);
        scanf("%lf", arr+i);
    }

    printf("Unsorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    insertionSort(arr, n);

    printf("\nSorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    printf("\n");
    free(arr);
    return 0;
}

/* computational complexity:
 * sum from 1 to n (sum(0 to i(3)) = n*(n/2)*3 ~= n^2
 * */