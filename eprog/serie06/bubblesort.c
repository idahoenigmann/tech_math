//
// Created by ida on 17.11.20.
//

#include <stdio.h>
#include <stdlib.h>

void bubbleSort(double* x, int n) {
    for(int i=0; i < n; i++) {
        for (int j=0; j < n - 1; j++) {
            if (x[j]>x[j+1]) {
                double tmp = x[j+1];
                x[j+1] = x[j];
                x[j] = tmp;
            }
        }
    }
}

int main() {
    printf("Sorts a given vector using bubble sort.\n");

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

    bubbleSort(arr, n);

    printf("\nSorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    printf("\n");
    free(arr);
    return 0;
}

/* Computational complexity:
 * sum(0 to n(sum(0 to n(6))) ~= n^2
 */