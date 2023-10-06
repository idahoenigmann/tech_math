//
// Created by ida on 24.10.20.
//

#include <stdio.h>
#include <assert.h>

int sqrtboundaries(double x) {
    assert(x >= 0);

    int res = 0;
    while (res * res <= x) {
        res++;
    }
    return res - 1;
}

int main() {
    printf("Find k, so that k <= sqrt(x) < k + 1 for a given x.\n");
    double x = 0;

    printf("Please enter a value for x: ");
    scanf("%lf", &x);

    printf("The result is %d.\n", sqrtboundaries(x));
    return 0;
}