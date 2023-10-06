//
// Created by ida on 24.10.20.
//

#include <stdio.h>

double scanfpositive() {
    double x = 0;

    do {
        printf("Please enter a positive number: ");
        scanf("%lf", &x);
    } while (x <= 0);

    return x;
}

int main() {
    scanfpositive();
    return 0;
}