//
// Created by ida on 03.11.20.
//

#include <stdio.h>
#define N 3

double scalarProduct(double x[], double y[], int n) {
    double res = 0;
    for (int i=0; i < n; i++) {
        res += x[i] * y[i];
    }
    return res;
}

int main() {
    printf("Calculate the scalar product of two vectors of size %d.\n", N);
    double y[N];
    double x[N];

    for (int i=0; i < N; i++) {
        x[i] = 0;
        printf("Please enter a value for x[%d]: ", i + 1);
        // x is a pointer to the first element of x[N]; x + i points to the i th element behind x
        scanf("%lf", x + i);
    }
    printf("\n");

    for (int i=0; i < N; i++) {
        y[i] = 0;
        printf("Please enter a value for y[%d]: ", i + 1);
        // y is a pointer to the first element of y[N]; x + i points to the i th element behind y
        scanf("%lf", y + i);
    }

    printf("\n%f\n", scalarProduct(x, y, N));

    return 0;
}

/* Test:
 * x = 1, 1, 1; y = 1, 1, 1
 * x = 3, 2.8, 1.01237; y = 2.1, 0.0, 99999.999
 *
 * x = 10, 5; y = 5, 10
 * x = 10, 1000; y = 1, 1
 */