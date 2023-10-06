//
// Created by ida on 14.01.21.
//

#include <iostream>
#include "ReducedMatrix.h"

using namespace std;

int main() {
    LowerTriangularMatrix lm(4);

    cout << lm.size() << endl;

    int tmp{1};
    for (int i{0}; i < 4; i++) {
        for (int j{0}; j <= i; j++) {
            lm(i, j) = tmp;
            tmp++;
        }
    }

    for (int i{0}; i < 4; i++) {
        for (int j{0}; j <= i; j++) {
            cout << lm(i, j) << ", ";
        }
        cout << endl;
    }

    SymmetricMatrix sm1(3);
    SymmetricMatrix sm2(3);

    cout << sm1.size() << endl;

    tmp = 1;
    for (int i{0}; i < 3; i++) {
        for (int j{0}; j <= i; j++) {
            sm1(i, j) = tmp;
            tmp++;
        }
    }

    sm2(0, 0) = 1;
    sm2(1, 0) = 0;
    sm2(1, 1) = 1;
    sm2(2, 0) = 0;
    sm2(2, 1) = 0;
    sm2(2, 2) = 1;

    for (int i{0}; i < 3; i++) {
        for (int j{0}; j < 3; j++) {
            cout << sm2(i, j) << ", ";
        }
        cout << endl;
    }

    cout << sm2.powerIteration(0.001) << endl;

    LowerTriangularMatrix cholesky {sm2.computeCholesky()};

    for (int i{0}; i < cholesky.size(); i++) {
        for (int j{0}; j < cholesky.size(); j++) {
            cout << cholesky(i, j) << ", ";
        }
        cout << endl;
    }

    return 0;
}