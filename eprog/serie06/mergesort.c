//
// Created by ida on 17.11.20.
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void merge(double* arr_left, int arr_left_len, double* arr_right, int arr_right_len, double* ret) {
    int idx_left = 0;
    int idx_right = 0;
    int idx = 0;

    while (idx_left < arr_left_len && idx_right < arr_right_len) {
        if (arr_left[idx_left] <= arr_right[idx_right]) {
            ret[idx] = arr_left[idx_left];
            idx += 1;
            idx_left += 1;
        } else {
            ret[idx] = arr_right[idx_right];
            idx +=1;
            idx_right += 1;
        }
    }

    // copy the rest
    if (idx_left < arr_left_len) {
        for (int i = idx_left; i < arr_left_len; ++i) {
            ret[idx] = arr_left[i];
            idx += 1;
        }
    } else if (idx_right < arr_right_len) {
        for (int i = idx_right; i < arr_right_len; ++i) {
            ret[idx] = arr_right[i];
            idx += 1;
        }
    }
}

/*
 * Computational complexity:
 * sum from 0 to arr_left_len + arr_right_len(4) = len*4
 */

void mergeSort_(double* arr, int arr_len, double* tmp) {
    int middle = arr_len / 2;
    if (middle == 0) {
        return;
    }

    double* left = arr;
    int left_len = middle;

    double* right = arr + middle;
    int right_len = arr_len - middle;

    mergeSort_(left, left_len, tmp);
    mergeSort_(right, right_len, tmp);

    merge(left, left_len, right, right_len, tmp);

    // copy result to original array
    for (int i = 0; i < arr_len; ++i) {
        arr[i] = tmp[i];
    }
}

/*
 * Computational complexity:
 * log n*(3+len*4+sum from 0 to len(1)) = log n*(len*5+3) ~= log n * n
 */

double* mergeSort(double* x, int n) {
    double* tmp = malloc(n*sizeof(double));
    mergeSort_(x, n, tmp);
    free(tmp);

    return x;
}

int main() {
    printf("Sorts a given vector using merge sort.\n");

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

    arr = mergeSort(arr, n);

    printf("\nSorted vector:\n");
    for(int i=0; i < n; i++) {
        printf("%f, ", arr[i]);
    }

    printf("\n");
    free(arr);
    return 0;
}