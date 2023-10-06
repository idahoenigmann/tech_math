#include <stdio.h>

int main() {
    printf("Calculate area of trapezoid.\n");

    double B = 0;
    double b = 0;
    double h = 0;

    printf("base length: ");
    scanf("%lf", &B);

    if (B < 0) {
        printf("Base length can not be smaller than 0.\n");
        return 1;
    }

    printf("top length: ");
    scanf("%lf", &b);

    if (b < 0) {
        printf("Top length can not be smaller than 0.\n");
        return 1;
    }

    printf("height: ");
    scanf("%lf", &h);

    if (h < 0) {
        printf("Height can not be smaller than 0.\n");
        return 1;
    }

    printf("The area is %f.\n", h * (B + b) / 2);

    return 0;
}