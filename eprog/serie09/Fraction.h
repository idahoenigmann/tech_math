//
// Created by ida on 09.12.20.
//

#ifndef SERIE09_123_FRACTION_H
#define SERIE09_123_FRACTION_H

#include <stdexcept>
#include "utils.h"

class Fraction {
public:
    Fraction() = default;
    Fraction(int numerator, int denominator);
    ~Fraction() = default;
    void reduce();
    int getNumerator();
    unsigned int getDenominator();
private:
    int numerator = 0;
    unsigned int denominator = 1;
};

Fraction addFractions(Fraction& a, Fraction& b);


#endif //SERIE09_123_FRACTION_H
