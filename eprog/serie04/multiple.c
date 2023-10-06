//
// Created by ida on 03.11.20.
//

#include <stdio.h>
#include <assert.h>

void multiple(int k, int nmax) {
    assert(k > 0);
    assert(nmax > k);
    int n = 1;
    while (k * n < nmax) {
        printf("%d x %d = %d\n", n, k, k * n);
        n++;
    }
}

int main() {
    printf("Computes multiples of k smaller than nmax.\n");
    int k = 0;
    int nmax = 0;

    printf("Please enter a value for k: ");
    scanf("%d", &k);

    printf("Please enter a value for nmax: ");
    scanf("%d", &nmax);

    multiple(k, nmax);
    return 0;
}

/* Test:
 * 5, 19
 * 2, 10
 * 1, 30
 * -1, 1
 */