//
// Created by ida on 16.11.20.
//

#include <stdio.h>
#include <stdlib.h>

double* cut(double* x, int* n, double cmin, double cmax) {
    int idx=0;
    for (int i=0; i < *n; i++) {
        if (x[i] >= cmin && x[i] <= cmax) {
            x[idx] = x[i];
            idx++;
        }
    }
    x = realloc(x,idx*sizeof(double));
    *n = idx;
    return x;
}

int main() {
    printf("Removes all values smaller or larger than a given number from the vector of size n.\n");
    double* arr;
    int n = 0;
    double min = 0;
    double max = 0;

    printf("Please enter a value for n: ");
    scanf("%d",&n);

    printf("Please enter a value for the minimum: ");
    scanf("%lf", &min);

    printf("Please enter a value for the maximun: ");
    scanf("%lf", &max);

    arr = malloc(n*sizeof(double));

    for (int i=0; i < n; i++) {
        printf("Please enter a value for x[%d]: ", i);
        scanf("%lf",arr+i);
    }

    for (int i=0; i < n; i++) {
        printf("%f, ",arr[i]);
    }
    printf("\n");

    arr = cut(arr, &n, min, max);

    for (int i=0; i < n; i++) {
        printf("%f, ",arr[i]);
    }
    printf("\n");

    free(arr);
    return 0;
}