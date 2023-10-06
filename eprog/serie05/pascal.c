//
// Created by ida on 09.11.20.
//

#include <stdio.h>

int factorial(int n) {
    int res = 1;
    for (int i=0; i < n; i++) {
        res*=n-i;
    }
    return res;
}

void pascal(int n) {
    for (int i = 0; i < n; i++) {
        for (int j=0; j < 2*(n-i); j++) {
            printf(" ");
        }
        for (int j=0; j <= i; j++) {
            int noverk = (double)(factorial(i))/(factorial(j)*factorial(i-j));
            printf("%4d", noverk);
        }
        printf("\n");
    }
}

int main() {
    printf("Print the first n lines of pascals triangle.\n");
    int n = 0;

    printf("Please enter a value for n = ");
    scanf("%d",&n);
    pascal(n);

    return 0;
}

/* Tested:
 * 5
 * 1
 * 3
 * 0
 * */