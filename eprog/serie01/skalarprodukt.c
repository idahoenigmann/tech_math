#include <stdio.h>

int main() {
    printf("Calculate dot product of vector u = (a,b,c) and vector v = (x,y,z).\n");

    double a = 0;
    double b = 0;
    double c = 0;

    double x = 0;
    double y = 0;
    double z = 0;

    printf("a = ");
    scanf("%lf", &a);

    printf("b = ");
    scanf("%lf", &b);

    printf("c = ");
    scanf("%lf", &c);

    printf("x = ");
    scanf("%lf", &x);

    printf("y = ");
    scanf("%lf", &y);

    printf("z = ");
    scanf("%lf", &z);

    printf("The dot product is %f.\n", a * x + b * y + c * z);

    return 0;
}