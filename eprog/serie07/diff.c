//
// Created by ida on 24.11.20.
//

#include <stdio.h>
#include <math.h>
#include <assert.h>


double f(double x) {
    return x * x * x;
}

double phi(double (*f)(double), double x, double h) {
    assert(h > 0);
    return (f(x + h) - f(x)) / h;
}

double diff(double (*f)(double), double x, double h0, double tau) {
    double phi_x;
    double phi_x1;
    double prev_h = h0;

    assert(tau > 0);
    assert(h0 > 0);

    while (1) {
        prev_h = prev_h / 2;
        phi_x = phi(f, x, prev_h);
        phi_x1 = phi(f, x, prev_h / 2);

        if (fabs(phi_x) <= tau) {
            if (fabs(phi_x - phi_x1) <= tau) {
                return phi_x;
            }
        } else {
            if (fabs(phi_x - phi_x1) <= tau * fabs(phi_x)) {
                return phi_x;
            }
        }
    }
}

int main() {
    printf("Approximate the derivative f'(x).\n");

    double x = 0;
    double h0 = 0;
    double tau = 0;

    printf("Please enter a value for x: ");
    scanf("%lf", &x);

    printf("Please enter a value for h0: ");
    scanf("%lf", &h0);

    printf("Please enter a value for tau: ");
    scanf("%lf", &tau);

    double res = diff(f, x, h0, tau);

    printf("%f\n", res);

    return 0;
}

/* Tested:
 * x = 0; h0 = 1; tau = 0.1
 * x = 10; h0 = 1; tau = 0.1
 * x = 0; h0 = 10; tau = 0.1
 * x = 0; h0 = 1; tau = 1
 */