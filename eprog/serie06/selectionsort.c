//
// Created by ida on 17.11.20.
//

#include <stdio.h>
#include <stdlib.h>

void selectionSort(double* x, int n) {
    for (int i=0; i < n ; i++) {
        double min = x[i];
        int min_idx = i;
        for(int j=i; j < n; j++) {
            if (x[j] < min) {
                min = x[j];
                min_idx = j;
            }
        }
        double tmp = x[min_idx];
        x[min_idx] = x[i];
        x[i] = tmp;
    }
}

int main() {
    printf("Sorts a given vector using selection sort.\n");

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

    selectionSort(arr, n);

    printf("\nSorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    printf("\n");
    free(arr);
    return 0;
}

/* computational complexity:
 * sum from 0 to n (sum(i to n(3)+3) = n*n*3+3 = =O(n^2)
 * */