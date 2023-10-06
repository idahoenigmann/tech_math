//
// Created by ida on 09.11.20.
//

#include <stdio.h>
#include <time.h>
#define N 8

double max_(double x[], int n) {
    double res = x[0];
    for (int i=0; i < n; i++) {
        if (x[i] > res) {
            res = x[i];
        }
    }
    return res;
}

int maxcompare(double a[], double b[], int n) {
    double max;
    double max_a = max_(a,n);
    double max_b = max_(b,n);
    if (max_a >= max_b) {
        max = max_a;
    } else {
        max = max_b;
    }

    int res = 0;
    for (int i=0; i < n; i++) {
        if (a[i] == max && b[i] == max) {
            res++;
        }
    }
    return res;
}

int main() {
    printf("Return how often the maximum of two vectors occurs in the same position.\n");

    double a[N];
    double b[N];
    int res = 0;
    clock_t start = 0;
    clock_t end = 0;

    for (int i = 0; i < N; ++i) {
        printf("Please enter a value for a[%d]: ", i);
        scanf("%lf",a+i);
    }
    printf("\n");

    for (int i = 0; i < N; ++i) {
        printf("Please enter a value for b[%d]: ", i);
        scanf("%lf",b+i);
    }
    printf("\n");

    start = clock();
    res = maxcompare(a,b,N);
    end = clock();

    printf("%d\n", res);
    printf("The calculation took %1.2f\n",(double)(end-start)/CLOCKS_PER_SEC);

    return 0;
}