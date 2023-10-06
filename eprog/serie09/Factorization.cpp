//
// Created by ida on 09.12.20.
//

#include "Factorization.h"

using namespace std;

Factorization::Factorization(unsigned int number) {
    setNumber(number);
}

Factorization::~Factorization() {
    delete[] prime_factors;
    delete[] multiplicities;
    cnt_prime_factors = 0;
}

/**
 * Recomposes the original integer out of multiplicities and prime_factors
 * @return Original int
 */
unsigned int Factorization::recomposeInteger() {
    unsigned int acc = 1;

    for (int i = 0; i < (int)cnt_prime_factors; i++) {
        for (int j = 0; j < (int)multiplicities[i]; ++j) {
            acc *= prime_factors[i];
        }
    }

    return acc;
}

/**
 * Get a number(int) as input and calculates the prime factors and multiplicities.
 * @param number Int, to be split up into prime factors
 */
void Factorization::setNumber(unsigned int number) {
    IntVector prime_numbers = IntVector((int) number);

    int idx = 0;
    int *prime_factors_tmp = new int[prime_numbers.getLength()];
    int *multiplicity_tmp = new int[prime_numbers.getLength()];

    for (int i = 0; i < (int)prime_numbers.getLength(); i++) {
        int curr_prime_factor = prime_numbers.getCoefficient(i);
        if (number % curr_prime_factor == 0) {
            prime_factors_tmp[idx] = curr_prime_factor;
            multiplicity_tmp[idx] = 1;
            unsigned int tmp_number = number / curr_prime_factor;

            while (tmp_number % curr_prime_factor == 0) {
                tmp_number /= curr_prime_factor;
                multiplicity_tmp[idx]++;
            }

            idx++;
        }
    }

    delete[] prime_factors;
    delete[] multiplicities;

    prime_factors = new unsigned int[idx];
    multiplicities = new unsigned int[idx];
    cnt_prime_factors = idx;

    for (int i = 0; i < idx; i++) {
        prime_factors[i] = prime_factors_tmp[i];
        multiplicities[i] = multiplicity_tmp[i];
    }

    delete[] prime_factors_tmp;
    delete[] multiplicity_tmp;
}

unsigned int Factorization::getPrimeFactorCnt() {
    return cnt_prime_factors;
}


unsigned int Factorization::getPrimeFactor(int idx) {
    if (idx >= (int)cnt_prime_factors) {
        throw logic_error("Index out of bounds.");
    }
    return prime_factors[idx];
}


unsigned int Factorization::getMultiplicity(int idx) {
    if (idx >= (int)cnt_prime_factors) {
        throw logic_error("Index out of bounds.");
    }
    return multiplicities[idx];
}

