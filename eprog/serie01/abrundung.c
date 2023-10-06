#include <stdio.h>

int main() {
    printf("Floors a given number.\n");

    double x = 0;

    printf("x = ");
    scanf("%lf", &x);

    printf("%d\n", (int)x);

    /*
    if (x >= 0) {
        printf("%d\n", (int)x);
    } else {
        printf("%d\n", (int)x - 1);
    }
    */

    return 0;
}