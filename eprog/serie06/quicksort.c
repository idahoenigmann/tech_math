//
// Created by ida on 17.11.20.
//

#include <stdio.h>
#include <stdlib.h>

int partition(double* x, int start, int end) {
    double pivot = x[end];
    int i = start - 1;
    for (int j=start; j < end; j++) {
        if (x[j] <= pivot) {
            i++;
            double tmp = x[i];
            x[i] = x[j];
            x[j] = tmp;
        }
    }
    double tmp = x[i+1];
    x[i+1] = x[end];
    x[end] = tmp;
    return i+1;
}

/* Computational complexity:
 * 1+ sum from start to end(4) + 4 = 5 + (end - start)*4
 */

void quickSort_(double* x, int start, int end) {
    if (start < end) {
        int p = partition(x, start, end);
        quickSort_(x, start, p - 1);
        quickSort_(x, p + 1, end);
    }
}

/* computational complexity:
 * n * (end - start)*4 + 3 ~= n^2
 */

void quickSort(double* x, int n) {
    quickSort_(x, 0, n - 1);
}

int main() {
    printf("Sorts a given vector using quick sort.\n");

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

    quickSort(arr, n);

    printf("\nSorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    printf("\n");
    free(arr);
    return 0;
}