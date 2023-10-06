//
// Created by ida on 21.12.20.
//

#ifndef SERIE11_POLYNOMIAL_H
#define SERIE11_POLYNOMIAL_H

#include <stdexcept>
#include <iostream>
#include <cmath>

#define MAX(a,b) ((a) < (b) ? (b) : (a))

class Polynomial {
public:
    Polynomial(unsigned int degree, double coefficient);
    ~Polynomial();
    Polynomial(const Polynomial &other);
    Polynomial& operator=(const Polynomial &rhs);

    unsigned int degree() const;

    double& operator[](unsigned int idx);
    const double& operator[](unsigned int idx) const;

    bool operator==(const Polynomial& other);

    double operator()(int k, double x) const;
    double operator()(double x) const;
    Polynomial operator()(int k) const;

    double computeIntegral(double alpha, double beta) const;

    double computeZero(double x0, double tau) const;

    Polynomial(unsigned int degree, const std::string& function);

private:
    unsigned int degree_ = 0;
    double* coefficients = nullptr;
};

std::ostream& operator<<(std::ostream& stream, const Polynomial& polynomial);

Polynomial operator+(const Polynomial& p1, const Polynomial& p2);
Polynomial operator+(const Polynomial& p, double d);
Polynomial operator+(double d, const Polynomial& p);

Polynomial operator*(const Polynomial& p1, const Polynomial& p2);
Polynomial operator*(const Polynomial& p, double d);
Polynomial operator*(double d, const Polynomial& p);


#endif //SERIE11_POLYNOMIAL_H
