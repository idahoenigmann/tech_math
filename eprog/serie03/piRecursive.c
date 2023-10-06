//
// Created by ida on 24.10.20.
//

#include <stdio.h>

double P(int n) {
    if (n == 0) {
        return 4;
    }

    double res = 4.0 / (2.0 * n + 1.0);

    if (n % 2 == 1) {
        res = res * -1.0;
    }

    return res + P(n - 1);
}

int main() {
    printf("Calculate pi using the Leibniz formula with n terms.\n");

    int n = 0;
    printf("Please enter a value for n: ");
    scanf("%d", &n);

    printf("Pi approximation: %f\n", P(n));
    return 0;
}