//
// Created by ida on 21.12.20.
//

#include "Polynomial.h"

using namespace std;

Polynomial::Polynomial(unsigned int degree, double coefficient) {
    this->degree_ = degree;
    this->coefficients = new double[this->degree() + 1];
    for(int i{0}; i < this->degree() + 1; i++) {
        (*this)[i] = coefficient;
    }
}

Polynomial::~Polynomial() {
    delete[] coefficients;
}

Polynomial::Polynomial(const Polynomial &other) {
    this->degree_ = other.degree();
    this->coefficients = new double[degree() + 1];
    for(int i{0}; i < degree() + 1; i++) {
        (*this)[i] = other[i];
    }
}

Polynomial& Polynomial::operator=(const Polynomial &rhs) {
    if (this != &rhs) {
        if (rhs.degree() != degree()) {
            delete[] coefficients;
            degree_ = rhs.degree();
            coefficients = new double[degree() + 1];
        }
        for (int i{0}; i < degree() + 1; i++) {
            (*this)[i] = rhs[i];
        }
    }
    return *this;
}

unsigned int Polynomial::degree() const {
    return degree_;
}

const double& Polynomial::operator[](unsigned int idx) const {
    if (idx >= degree() + 1) {
        throw logic_error("Index out of bound.");
    }
    return coefficients[idx];
}

double& Polynomial::operator[](unsigned int idx) {
    if (idx >= degree() + 1) {
        throw logic_error("Index out of bound.");
    }
    return coefficients[idx];
}

bool Polynomial::operator==(const Polynomial &other) {
    if (other.degree() != degree()) {
        return false;
    }
    double accuracy = 0.01;
    for (int i{0}; i < degree() + 1; i++) {
        if (fabs(other[i] - (*this)[i]) > accuracy) {
            return false;
        }
    }
    return true;
}

double Polynomial::operator()(int k, double x) const {
    Polynomial tmp{(*this)(k)};
    return tmp(x);
}

double Polynomial::operator()(double x) const {
    double res{0};
    
    for (int i{0}; i < degree() + 1; i++) {
        res += (*this)[i] * pow(x, i);
    }
    
    return res;
}

Polynomial Polynomial::operator()(int k) const {
    if (k == 0) {
        return *this;
    }
    Polynomial res(MAX(degree() - 1, 1), 0);
    
    for (int i{1}; i < degree() + 1; i++) {
        res[i - 1] = (*this)[i] * i;
    }
    
    return res(k - 1);
}

double Polynomial::computeIntegral(double alpha, double beta) const {
    if (beta <= alpha) {
        throw logic_error("Beta may not be smaller than alpha.");
    }

    double res{0};

    for (int i{0}; i < degree() + 1; i++) {
        res += (*this)[i] * (pow(beta, i + 1) - pow(alpha, i + 1)) / (i + 1);
    }

    return res;
}

double Polynomial::computeZero(double x0, double tau) const {
    if (tau <= 0) {
        throw logic_error("Tau must be bigger than 0.");
    }
    double last_x{};
    double x{x0};
    while (true) {
        last_x = x;
        x = last_x - (*this)(last_x) / (*this)(1, last_x);

        if (fabs((*this)(x)) <= tau) {
            break;
        }
        if (fabs(x - last_x) <= tau) {
            break;
        }
    }
    return x;
}

Polynomial::Polynomial(unsigned int degree, const std::string& function) {
    this->degree_ = degree;
    this->coefficients = new double[this->degree() + 1];

    int function_type{};

    if (function == "sin") {
        function_type = 0;
    } else if (function == "cos") {
        function_type = 1;
    } else if (function == "exp") {
        function_type = 4;
    } else {
        throw logic_error("function must be either sin, cos or exp.");
    }

    double factorial{1};

    for (int i{0}; i < this->degree() + 1; i++) {
        if (i != 0) {
            factorial *= i;
        }

        double f0{};

        switch (function_type) {
            case 0: // sin
                f0 = 0;
                function_type++;
                break;
            case 1: // cos
                f0 = 1;
                function_type++;
                break;
            case 2: // - sin
                f0 = 0;
                function_type++;
                break;
            case 3: // - cos
                f0 = -1;
                function_type = 0;
                break;
            case 4: // exp
                f0 = 1;
                break;
        }

        (*this)[i] = f0 / factorial;
    }
}

std::ostream& operator<<(ostream &stream, const Polynomial& polynomial) {
    if (polynomial.degree() >= 1) {
        stream << ((polynomial[0] < 0) ? "- " : "") << fabs(polynomial[0]);
        for (int i{1}; i < polynomial.degree() + 1; i++) {
            stream << ((polynomial[i] < 0) ? " - " : " + ") << fabs(polynomial[i]) << "x^" << i;
        }
    }
    return stream;
}

Polynomial operator+(const Polynomial& p1, const Polynomial& p2) {
    Polynomial res(MAX(p1.degree(), p2.degree()),0);
    for (int i{0}; i < p1.degree() + 1; i++) {
        res[i] += p1[i];
    }
    for (int i{0}; i < p2.degree() + 1; i++) {
        res[i] += p2[i];
    }
    return res;
}

Polynomial operator+(const Polynomial& p, double d) {
    if (p.degree() >= 1) {
        Polynomial res(p);

        res[0] += d;
        return res;
    } else {
        return Polynomial(0, d);
    }
}

Polynomial operator+(double d, const Polynomial& p) {
    return p + d;
}

Polynomial operator*(const Polynomial& p1, const Polynomial& p2) {
    Polynomial res(p1.degree() + p2.degree(),1);
    for (int i{0}; i < p1.degree() + 1; i++) {
        res[i] *= p1[i];
    }
    for (int i{0}; i < p2.degree() + 1; i++) {
        res[i] *= p2[i];
    }
    return res;
}

Polynomial operator*(const Polynomial& p, double d) {
    Polynomial res(p);

    for (int i{0}; i < p.degree() + 1; i++) {
        res[i] *= d;
    }

    return res;
}

Polynomial operator*(double d, const Polynomial& p) {
    return p * d;
}