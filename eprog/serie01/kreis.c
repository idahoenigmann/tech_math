#include <stdio.h>
#include <math.h>

int main() {
    printf("Calculate area and circumference of a circle.\n");

    double r = 0;
    double area = 0;
    double circumference = 0;

    printf("Please enter the radius: ");
    scanf("%lf", &r);

    if (r < 0) {
        printf("Radius can not be smaller than 0.\n");
        return 1;
    }

    area = r * r * M_PI;
    circumference = 2 * r * M_PI;

    printf("The area is %f.\n", area);
    printf("The circumference is %f.\n", circumference);

    return 0;
}