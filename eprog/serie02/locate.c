#include <stdio.h>

int main() {
    printf("Check whether a point (x,y) is inside or outside a square with vertices (0, 0), (L, 0), (0, L) and (L, L).\n");

    double l = 0;
    double x = 0;
    double y = 0;

    printf("Please enter the side length of the square. L: ");
    scanf("%lf", &l);

    printf("Please enter the x-coordinate of the point. x: ");
    scanf("%lf", &x);

    printf("Please enter the y-coordinate of the point. y: ");
    scanf("%lf", &y);

    if (x < 0 || y < 0 || x > l || y > l) {
        printf("The point (%f, %f) lies outside of the square.\n", x, y);
    } else if (x == 0 || y == 0 || x == l || y == l) {
        printf("The point (%f, %f) lies on the boundary of the square.\n", x, y);
    } else {
        printf("The point (%f, %f) lies inside the square.\n", x, y);
    }

    return 0;
}