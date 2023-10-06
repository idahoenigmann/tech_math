//
// Created by ida on 24.10.20.
//

#include <stdio.h>

int product(int x, int y) {
    int res = 0;

    while (y > 0) {
        res = res + x;
        y--;
    }

    return res;
}

int main() {
    printf("Calculate x*y.\n");
    int x = 0;
    int y = 0;

    printf("Please enter a value for x: ");
    scanf("%d", &x);
    printf("Please enter a value for y: ");
    scanf("%d", &y);

    printf("The result is %d.\n", product(x, y));
    return 0;
}