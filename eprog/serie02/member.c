#include <stdio.h>

double member(int n) {
    if (n % 2 == 0) {
        return 1.0 / (n + 2.0);
    } else {
        return -1.0 / (n + 2.0);
    }
}


int main() {
    printf("compute a(n)=(-1)^n/(n+2) for a given n.\n");

    int n = 0;

    printf("Please enter n: ");
    scanf("%d", &n);

    printf("a(%d)=%f\n", n, member(n));

    return 0;
}