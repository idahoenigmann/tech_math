#include <stdio.h>

int main() {
    printf("Calculate zero of y=mx+q.\n");

    double m = 0;
    double q = 0;

    printf("m = ");
    scanf("%lf", &m);

    if (m == 0) {
        printf("m can not be 0.\n");
        return 1;
    }

    printf("q = ");
    scanf("%lf", &q);

    printf("Zero is at (%f,0).\n", -q / m);

    return 0;
}