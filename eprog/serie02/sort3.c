#include <stdio.h>

int main() {
    printf("Sort three numbers x, y, z.\n");

    double x = 0;
    double y = 0;
    double z = 0;

    printf("Please enter the first number.  x: ");
    scanf("%lf", &x);

    printf("Please enter the second number. y: ");
    scanf("%lf", &y);

    printf("Please enter the third number.  z: ");
    scanf("%lf", &z);

    if (x > y) {
        if (x > z) {
            printf("%f, ", x);
            if (y > z) {
                printf("%f, ", y);
                printf("%f\n", z);
            } else { // z > y
                printf("%f, ", z);
                printf("%f\n", y);
            }
        } else { // z > x
            printf("%f, ", z);
            printf("%f, ", x);
            printf("%f\n", y);
        }
    } else { // y > x
        if (y > z) {
            printf("%f, ", y);
            if (x > z) {
                printf("%f, ", x);
                printf("%f\n", z);
            } else { // z > x
                printf("%f, ", z);
                printf("%f\n", x);
            }
        } else { // z > y
            printf("%f, ", z);
            printf("%f, ", y);
            printf("%f\n", x);
        }
    }

    return 0;
}