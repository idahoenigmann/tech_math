//
// Created by ida on 09.11.20.
//

#include <stdio.h>
#define N 3

double energy(double x[], int n) {
    double res = 0;
    for (int j=0; j < n; j++) {
        res += x[j] * x[j];
    }
    return res;
}

int main() {
    printf("Computes the energy of a given vector of size %d.\n", N);
    double x[N];

    for (int i=0; i < N; i++) {
        x[i] = 0;
        printf("Please enter x[%d]=", i);
        scanf("%lf", x+i);
    }

    printf("%f\n", energy(x, N));
    return 0;
}

/* Computational complexity:
 * sum from 1 to n of (3) = 3 * n
 * O = n
 *
 * 3 sec for n = 10^3=1000
 * how many sec for n = 10^4=10000: 30 sec
 * */