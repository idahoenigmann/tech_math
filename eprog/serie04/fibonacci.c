//
// Created by ida on 02.11.20.
//

#include <stdio.h>
#include <assert.h>

int fibonacci(int n, int type) {
    assert(n >= 0);

    if (n == 0) return 0;
    if (n == 1) return 1;

    if (type == 1) {
        return fibonacci(n - 1, 1) + fibonacci(n - 2, 1);
    } else if (type == 2) {
        int pprev = 0;
        int prev = 1;
        int result = 0;

        for (int i = 0; i < n; i++) {
            result = prev + pprev;
            prev = pprev;
            pprev = result;
        }

        return result;
    } else {
        printf("Types different from 1, 2, 3 are not supported.\n");
        return -1;
    }
}

int main() {
    printf("Calculate fibonacci sequence. x(n)\n");

    int n = 0;

    printf("Please enter a value for n: ");
    scanf("%d", &n);

    printf("Method 1: The result is %d.\n", fibonacci(n, 1));
    printf("Method 2: The result is %d.\n", fibonacci(n, 2));

    return 0;
}

/* Test:
 * 0, 1, 5, 10, 30
 */