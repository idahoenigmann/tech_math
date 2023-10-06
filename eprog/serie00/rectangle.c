#include <stdio.h>

int main() {
    double a = 0;
    double b = 0;
    double area = 0;

    printf("Calculates the area of a rectangle.\n");

    printf("Length a: ");
    scanf("%lf", &a);

    printf("Length b: ");
    scanf("%lf", &b);

    area = a * b;

    printf("Area: %lf\n", area);
    return 0;
}
