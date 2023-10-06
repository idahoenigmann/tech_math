//
// Created by ida on 24.10.20.
//

#include <stdio.h>

int division(int m, int n) {
    if (m < n) {
        return 0;
    }

    return 1 + division(m - n, n);
}

int main() {
    printf("Calculate x / y\n");
    int m = 0;
    int n = 0;

    printf("Please enter x: ");
    scanf("%d", &m);

    printf("Please enter y: ");
    scanf("%d", &n);

    printf("The result is %d.\n", division(m, n));

    return 0;
}