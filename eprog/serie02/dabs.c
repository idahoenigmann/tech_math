#include <stdio.h>

double dabs(double x) {
    if (x < 0) {
        return -x;
    } else {
        return x;
    }
}

int main() {
    printf("computes the absolute value of a given number x.\n");

    double x = 0;

    printf("Please enter x: ");
    scanf("%lf", &x);

    printf("abs(%lf)=%lf\n", x, dabs(x));

    return 0;
}