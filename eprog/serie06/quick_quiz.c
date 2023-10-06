//
// Created by ida on 20.11.20.
//

#include <stdio.h>

void tripleSwap(double* x1, double* x2, double* x3) {
    double tmp = *x1;

    *x2 = *x3;
    *x3 = *x1;
    *x1 = *x2;
}

int main() {
    double x = 3;
    double y = 2;
    double z = 1;

    tripleSwap(&x, &y, &z);

    printf("%f %f %f\n", x, y, z);

    return 0;
}