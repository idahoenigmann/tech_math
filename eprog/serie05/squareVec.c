//
// Created by ida on 09.11.20.
//

#include <stdio.h>

void squareVec(double vec[], int n) {      // double vec[] instead of double vec & void instead of int
    int j=0;
    for(j=0; j<n; ++j) {              // ; instead of , & 0 instead of 1 & ++j instead of --j & n instead of dim
        vec[j] = vec[j] * vec[j];    // remove & and *
    }
    return;                 // return instead of return vec (or nothing)
}

int main() {
    double vec[3] = {-1.0,2.0,0.0};
    int j=0;

    squareVec(vec, 3);
    for(j=0; j<3; ++j) {
        printf("vec[%d] = %f ",j,vec[j]);
    }
    printf("\n");
}