#include <stdio.h>

int main() {
    printf("Calculate p(x) = ax²+bx+c for a given x.\n");

    double a = 0;
    double b = 0;
    double c = 0;
    double x = 0;

    printf("a = ");
    scanf("%lf", &a);

    printf("b = ");
    scanf("%lf", &b);

    printf("c = ");
    scanf("%lf", &c);

    printf("x = ");
    scanf("%lf", &x);

    printf("p(%f) = %f\n", x, a * x * x + b * x + c);

    return 0;
}