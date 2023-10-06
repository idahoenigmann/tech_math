//
// Created by ida on 03.11.20.
//
#include <stdio.h>
#include <math.h>
#include <assert.h>
#define N 3

double pnorm(double x[], int n, int p) {
    assert(p >= 1);
    double res = 0;

    for (int i=0; i < n; i++) {
        res += pow(fabs(x[i]), p);
    }

    return pow(res, (1.0 / p));
}

int main() {
    printf("Calculate the lp-norm of a vector of size %d.\n", N);

    double x[N];
    int p = 0;

    for (int i=0; i < N; i++) {
        x[i] = 0;
        printf("Please enter a value for x[%d]: ", i + 1);
        // x is a pointer to the first element of x[N]; x + i points to the i th element behind x
        scanf("%lf", x + i);
    }

    printf("\nPlease enter a value for p: ");
    scanf("%d", &p);

    printf("\n%f\n", pnorm(x, N, p));

    return 0;
}

/* Test:
 * 1, 1, 1; p = 1 -> 1
 * 3.5, 2.5, 1.5; p = 1 -> 7.5
 * 2, 3, 4; p = 10 -> 4.022346
 * 2, 3, 4; p = 100 -> 4
 *
 * bei p -> unendlich geht pnorm -> max(vektor)
 */