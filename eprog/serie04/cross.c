//
// Created by ida on 02.11.20.
//

#include <stdio.h>
#include <assert.h>

void cross(int n) {
    assert(0 < n);
    assert(n <= 9);

    for (int i=0; i < n - 1; i++) {
        for (int j=0; j < i; j++) {
            printf(" ");
        }
        printf("%d", i + 1);
        for (int j=0; j < 2*(n-i) - 3; j++) {
            printf(" ");
        }
        printf("%d\n", i + 1);
    }

    for (int j=0; j < n - 1; j++) {
        printf(" ");
    }
    printf("%d\n", n);

    for (int i=n - 1; i > 0; i--) {
        for (int j=0; j < i - 1; j++) {
            printf(" ");
        }
        printf("%d", i);
        for (int j=0; j < 2*(n-i) - 1; j++) {
            printf(" ");
        }
        printf("%d\n", i);
    }
}

int main() {
    printf("Prints a cross of numbers of size n.\n");

    int n = 0;

    printf("Please enter a value for n: ");
    scanf("%d", &n);
    cross(n);
    return 0;
}

/* Test:
 * 6, 5, 1, 3
 */