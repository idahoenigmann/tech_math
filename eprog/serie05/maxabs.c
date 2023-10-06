//
// Created by ida on 09.11.20.
//

#include <stdio.h>
#include <math.h>
#define N 5

double maxabs(double x[], int n) {
    double res = x[0];
    double maxabs = fabs(x[0]);
    for (int i=0; i < n; i++) {
        if (fabs(x[i]) > maxabs) {
            maxabs = fabs(x[i]);
            res = x[i];
        }
    }
    return res;
}

int main() {
    printf("Return the value with the largest absolute value of an array of size %d.\n",N);
    double x[N];

    for(int i=0; i < N; i++) {
        x[i] = 0;
        printf("Please enter a value for x[%d]=",i);
        scanf("%lf",x+i);
    }

    printf("%f\n",maxabs(x,N));

    return 0;
}

/* Computational complexity:
 * sum from 1 to n (1+1+1+1+1+1) = n*6
 * O = n
 *
 * 3 sec for n = 10^3=1000
 * how many sec for n = 2 * 10^4=10000? 60 sec
 */