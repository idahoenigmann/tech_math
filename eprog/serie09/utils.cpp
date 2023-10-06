//
// Created by ida on 10.12.20.
//

#include "utils.h"

using namespace std;

int gcd(int a, int b) {
    if (a == 1) return b;
    if (b == 1) return a;

    int res = 1;

    Factorization a_factorization = Factorization(a);
    Factorization b_factorization = Factorization(b);

    // Iterate from back to front, adding prime factor if found.
    for (int i = (int) (a_factorization.getPrimeFactorCnt()) - 1; i >= 0; --i) {
        unsigned int current_prime_factor_a = a_factorization.getPrimeFactor(i);

        for (int j = 0; j < (int)b_factorization.getPrimeFactorCnt(); ++j) {
            unsigned int current_prime_factor_b = b_factorization.getPrimeFactor(j);

            if (current_prime_factor_a == current_prime_factor_b) {
                unsigned int current_multiplicity_a = a_factorization.getMultiplicity(i);
                unsigned int current_multiplicity_b = b_factorization.getMultiplicity(j);

                if (current_multiplicity_a < current_multiplicity_b) {
                    res *= (int) (current_prime_factor_b * current_multiplicity_a);
                } else {
                    res *= (int) (current_prime_factor_b * current_multiplicity_b);
                }
            }
        }
    }

    return res;
}

int lcm(int a, int b) {
    int acc_a = a;
    int acc_b = b;

    while (true) {
        if (acc_a == acc_b) {
            return acc_a;
        } else if (acc_a < acc_b) {
            acc_a += a;
        } else {
            acc_b += b;
        }
    }
}