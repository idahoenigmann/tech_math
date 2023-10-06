//
// Created by ida on 09.11.20.
//

#include <stdio.h>

double determinant(double a[]) {
    return a[0]*a[4]*a[8] + a[3]*a[7]*a[2] + a[6]*a[1]*a[5] - a[2]*a[4]*a[6] - a[5]*a[7]*a[0] - a[1]*a[3]*a[8];
}

int main() {
    //double a[] = {1,1,1,1,1,1,1,1,1};
    double a[] = {0.5,1,1.5,2,2.5,3,3.5,4,4.5};

    printf("%f\n",determinant(a));
    return 0;
}