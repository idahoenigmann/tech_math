#include <stdio.h>
#include <math.h>

int main() {
    printf("Convert angle into radians.\n");

    double angle = 0;

    printf("angle = ");
    scanf("%lf", &angle);

    printf("%lf\n", angle / 180.0 * M_PI);

    return 0;
}