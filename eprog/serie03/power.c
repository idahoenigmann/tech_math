//
// Created by ida on 24.10.20.
//

#include <stdio.h>
#include <assert.h>

double pow_(double x, int n) {
    double res = 1;
    while (n > 0) {
        res = res * x;
        n--;
    }
    return res;
}

int power(double x, double C) {
    assert(x > 1);
    assert(C > 0);

    int res = 0;
    while (1) {
        if (pow_(x, res) > C) {
            return res;
        }
        res++;
    }
}

int main() {
    printf("Find smallest n so that x^n > C.\n");
    double x = 0;
    double c = 0;

    printf("Please enter x: ");
    scanf("%lf", &x);
    printf("Please enter c: ");
    scanf("%lf", &c);

    printf("n is %d.\n", power(x, c));
    return 0;
}