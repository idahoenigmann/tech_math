#include <stdio.h>

double minabs(double x, double y) {
    if (x < 0) {
        x = -x;
    }
    if (y < 0) {
        y = -y;
    }
    if (x < y) {
        return x;
    } else {
        return y;
    }
}

int main() {
    printf("return number with smaller absolute value out of two numbers.\n");

    double x = 0;
    double y = 0;

    printf("Please enter the first number: ");
    scanf("%lf", &x);

    printf("Please enter the second number: ");
    scanf("%lf", &y);

    printf("%f\n", minabs(x, y));
    return 0;
}