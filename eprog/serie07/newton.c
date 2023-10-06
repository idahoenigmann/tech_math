//
// Created by ida on 24.11.20.
//

#include <stdio.h>
#include <math.h>
#include <assert.h>

double f(double x) {
    return 2 * x * x + 4 * x;
}

double fprime(double x) {
    return 4 * x + 4;
}

double newton(double (*f)(double), double (*fprime)(double), double x0, double tau) {
    double prev = x0;
    double x = x0;
    double fx = 0;

    assert(tau > 0);

    while(1) {
        prev = x;
        x = prev - f(prev) / fprime(prev);
        fx = f(x);

        if (fabs(fprime(x)) <= tau) {
            printf("The result is probably incorrect.\n");
            return x;
        } else if (fabs(x) <= tau) {
            if (fabs(fx) <= tau && fabs(x - prev) <= tau) {
                return x;
            }
        } else {
            if (fabs(fx) <= tau && fabs(x - prev) <= tau * fabs(x)) {
                return x;
            }
        }
    }
}

int main () {
    printf("Calculates the root by using the newton method.\n");

    double x0 = 0;
    double tau = 0;

    printf("Please enter a value for x0: ");
    scanf("%lf", &x0);

    printf("Please enter a value for tau: ");
    scanf("%lf", &tau);

    double xn = newton(f, fprime, x0, tau);

    printf("xn = %f, f(xn) = %f\n", xn, f(xn));

    return 0;
}

/* Tested:
 * x0 = 0; tau = 0.1
 * x0 = 1000; tau = 0.1
 * x0 = 0; tau = 1
 * x0 = 1000; tau = 1;
 * */