//
// Created by ida on 10.12.20.
//

#include <iostream>

#include "Stopwatch.h"

using namespace std;

int main() {
    Stopwatch S;
    double sum = 0.0;
    S.pushButtonStartStop();
    for(int j=1; j < 100*1000*1000; ++j) {
        sum += 1./j;
    }
    S.pushButtonStartStop();
    S.print();

    cout << sum << endl;

    S.pushButtonReset();

    S.print();

    return 0;
}

/* Computes the partial sum of the harmonic sequence. */