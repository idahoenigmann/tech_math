//
// Created by ida on 18.11.20.
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

double* unique(double* pdArr, int* piNumEl) {
    bubbleSort(pdArr, *piNumEl);

    int idx = 1;
    for (int i=1; i < *piNumEl; i++) {
        if (pdArr[idx-1] == pdArr[i]) continue;

        pdArr[idx] = pdArr[i];
        idx++;
    }
    pdArr = realloc(pdArr, sizeof(double)*idx);
    *piNumEl = idx;
    return pdArr;
}

int main() {
    printf("Sorts a given array and eliminates entries that appear more than once.\n");

    double* x;
    int n;

    printf("Please enter the value for the length of the array: ");
    scanf("%d",&n);

    x = malloc(n*sizeof(double));

    for(int i=0; i < n; i++) {
        printf("Please enter a value for x[%d]: ", i);
        scanf("%lf",x+i);
    }
    printf("\n");

    printf("Original array:\n");
    for (int i=0; i < n; i++) {
        printf("%f, ",x[i]);
    }
    printf("\n");

    x = unique(x, &n);

    printf("New array:\n");
    for (int i=0; i < n; i++) {
        printf("%f, ",x[i]);
    }
    printf("\n");

    return 0;
}