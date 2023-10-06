#include <stdio.h>

int main() {
    printf("Calculate next number in sequence a(n)=1/(n+2).\n");

    int n = 0;

    printf("n = ");
    scanf("%d", &n);

    printf("a(%d) = %f\n", n, 1.0 / (n + 2.0));

    return 0;
}