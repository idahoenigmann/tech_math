//
// Created by ida on 03.11.20.
//

#include <stdio.h>
#include <math.h>
#define N 3

double geometricMean(double x[], int n) {
    double res = 1;
    for (int i = 0; i < n; i++) {
        res *= x[i];
    }
    return pow(res, (1.0 / n));
}

int main() {
    printf("Calculates the geometric mean of a vector of size %d.\n", N);

    double x[N];

    for (int i=0; i < N; i++) {
        x[i] = 0;
        printf("Please enter a value for x[%d]: ", i + 1);
        // x is a pointer to the first element of x[N]; x + i points to the i th element behind x
        scanf("%lf", x + i);
    }

    printf("\n%f\n", geometricMean(x, N));
    return 0;
}

/* Test:
 * 10, 10, 10 -> 10
 * 1.5, 2.5, 3.5 -> 2.358847
 * 1.821376213, 1.821376213, 1.821376213 -> 1.821376213
 */