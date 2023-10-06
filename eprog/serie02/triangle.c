#include <stdio.h>

int main() {
    printf("Returns type of triangle formed by three edge lengths a,b,c.\n");

    double a = 0;
    double b = 0;
    double c = 0;

    printf("Please enter the first edge length.  a: ");
    scanf("%lf", &a);

    printf("Please enter the second edge length. b: ");
    scanf("%lf", &b);

    printf("Please enter the third edge length.  c: ");
    scanf("%lf", &c);

    if (a == b && b == c) {
        printf("equilateral ");
    } else if (a == b || b == c || a == c) {
        printf("isosceles ");
    } else {
        printf("scalene ");
    }

    if ((a * a + b * b == c * c) || (a * a + c * c == b * b) || (b * b + c * c == a * a)) {
        printf("right-angled ");
    }

    if (a + b == c || a + c == b || b + c == a) {
        printf("one-dimensional degenerated ");
    }

    if (a > b && a > c && b + c > a) {
        printf("impossible ");
    } else if (b > a && b > c && a + c > b) {
        printf("impossible ");
    } else if (c > a && c > b && a + b > c) {
        printf("impossible ");
    }

    printf("triangle\n");

    return 0;
}