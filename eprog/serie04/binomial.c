//
// Created by ida on 31.10.20.
//

#include <stdio.h>
#include <assert.h>

int factorial(int n) {
    int res = 1;

    for (int i=1; i <= n; i++) {
        res *= i;
    }

    return res;
}

int binomial(int n, int k, int type) {
    assert(0 <= k);
    assert(k <= n);

    if (type == 1) {
        printf("%d\n", factorial(n));
        return factorial(n) / (factorial(k) * factorial(n - k));
    } else if (type == 2) {
        int enumerator = 1;
        int denominator = 1;

        for (int i=0; i < k; i++) {
            enumerator *= n - i;
            denominator *= k - i;
        }

        return (int)(enumerator / denominator);
    } else if (type == 3) {
        if (k == 0 || n == k) return 1;
        if (n == 0) return 0;

        return binomial(n - 1, k, 3) + binomial(n - 1, k - 1, 3);
    } else {
        printf("Types different from 1, 2, 3 are not supported.\n");
        return -1;
    }
}

int main() {
    printf("Calculate binomial coefficient n over k.\n");

    int n = 0;
    int k = 0;

    printf("Please enter a value for n: ");
    scanf("%d", &n);
    printf("Please enter a value for k: ");
    scanf("%d", &k);

    printf("Method 1: The result is %d.\n", binomial(n, k, 1));
    printf("Method 2: The result is %d.\n", binomial(n, k, 2));
    printf("Method 3: The result is %d.\n", binomial(n, k, 3));

    return 0;
}

/* Test:
 * 0, 0 => 1
 * 1, 1 => 1
 * 5, 3 => 10
 * 10, 4 => 210
 * 20, 4 does not work, because factorial(20) is to large for an integer. :-(
 * */