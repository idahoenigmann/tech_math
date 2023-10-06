//
// Created by ida on 24.10.20.
//

#include <stdio.h>

double powN(double x, int n) {
    if (n == 0 && x != 0) {
        return 1.0;
    }

    if (n < 0) {
        return powN(1.0 / x, -n);
    }

    if (x == 0) {
        if (n > 0) {
            return 0.0;
        } else {
            printf("The value for 0^n is undefined when n <= 0.\n");
            return 0.0 / 0.0;
        }
    } else {
        return powN(x, n - 1) * x;
    }
}

int main() {
    printf("Calculate x^n.\n");
    double x = 0;
    int n = 0;

    printf("Please enter a value for x: ");
    scanf("%lf", &x);
    printf("Please enter a value for n: ");
    scanf("%d", &n);

    printf("The result is %f\n", powN(x, n));
    return 0;
}