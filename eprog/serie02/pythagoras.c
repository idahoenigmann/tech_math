#include <stdio.h>

int main() {
    printf("Check three numbers for a pythagorean triple.\n");

    // example of a pythagorean triple: 3, 4, 5

    int a = 0;
    int b = 0;
    int c = 0;

    printf("Please enter the first number: ");
    scanf("%d", &a);

    printf("Please enter the second number: ");
    scanf("%d", &b);

    printf("Please enter the third number: ");
    scanf("%d", &c);

    if (a >= 0 && b >= 0 && c >= 0) {
        if ((a * a + b * b == c * c) || (a * a + c * c == b * b) || (b * b + c * c == a * a)) {
            printf("The three numbers form a pythagorean triple.\n");
        } else {
            printf("The three numbers do not form a pythagorean triple.\n");
        }
    } else {
        printf("The three numbers can not be interpreted as the side lengths of a right triangle.\n");
    }


    return 0;
}