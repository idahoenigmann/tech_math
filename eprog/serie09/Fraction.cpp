//
// Created by ida on 09.12.20.
//

#include "Fraction.h"

using namespace std;

Fraction::Fraction(int numerator, int denominator) {
    if (denominator == 0) {
        throw logic_error("Division by zero!");
    }

    if (denominator < 0) {
        this->numerator = -numerator;
        this->denominator = -denominator;
    } else {
        this->numerator = numerator;
        this->denominator = denominator;
    }
}

void Fraction::reduce() {
    int gcd_num_denom = gcd(numerator, (int) denominator);
    numerator = numerator / gcd_num_denom;
    denominator = denominator / gcd_num_denom;
}

int Fraction::getNumerator() {
    return numerator;
}

unsigned int Fraction::getDenominator() {
    return denominator;
}


Fraction addFractions(Fraction &a, Fraction &b) {
    Fraction result = Fraction(a.getNumerator() * b.getDenominator() + b.getNumerator() * a.getDenominator(),
                               a.getDenominator() * b.getDenominator());
    result.reduce();

    return result;
}
