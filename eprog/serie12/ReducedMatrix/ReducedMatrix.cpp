//
// Created by ida on 14.01.21.
//

#include "ReducedMatrix.h"

using namespace std;

ReducedMatrix::ReducedMatrix(unsigned int coeffLen, double value) {
    this->coeff_len = coeffLen;
    coeff = new double[coeffLen * (coeffLen + 1) / 2];

    for (int i{0}; i < coeffLen * (coeffLen + 1) / 2; i++) {
        coeff[i] = value;
    }
}

ReducedMatrix::~ReducedMatrix() {
    delete[] coeff;
}

ReducedMatrix::ReducedMatrix(const ReducedMatrix& other) {
    this->coeff_len = other.coeff_len;
    coeff = new double [coeff_len * (coeff_len + 1) / 2];

    for (int i{0}; i < coeff_len * (coeff_len + 1) / 2; i++) {
        coeff[i] = other[i];
    }
}

ReducedMatrix &ReducedMatrix::operator=(const ReducedMatrix &rhs) {
    if (this != &rhs) {
        if (this->coeff_len != rhs.coeff_len) {
            delete [] coeff;
            this->coeff_len = rhs.coeff_len;
            coeff = new double[coeff_len * (coeff_len + 1) / 2];
        }
        for (int i{0}; i < coeff_len * (coeff_len + 1) / 2; i++) {
            coeff[i] = rhs[i];
        }
    }
    return *this;
}

int ReducedMatrix::size() const {
    return (int)coeff_len;
}

const double &ReducedMatrix::operator[](int idx) const {
    if (idx >= coeff_len * (coeff_len + 1) / 2) {
        throw logic_error("index out of bounds.");
    }
    return coeff[idx];
}

double &ReducedMatrix::operator[](int idx) {
    if (idx >= coeff_len * (coeff_len + 1) / 2) {
        throw logic_error("index out of bounds.");
    }
    return coeff[idx];
}

double &LowerTriangularMatrix::operator()(int row, int col) {
    if (row >= size() || col >= size()) {
        throw logic_error("index out of bound");
    }
    if (row < col) {
        return zero;            // Note: value of zero could be changed by this method
    }
    return (*this)[(row) * (row + 1) / 2 + (col)];
}

const double &LowerTriangularMatrix::operator()(int row, int col) const {
    if (row >= size() || col >= size()) {
        throw logic_error("index out of bound");
    }
    if (row < col) {
        return const_zero;
    }
    return (*this)[(row) * (row + 1) / 2 + (col)];
}

double &SymmetricMatrix::operator()(int row, int col) {
    if (row >= size() || col >= size()) {
        throw logic_error("index out of bound");
    }
    if (row < col) {
        return (*this)[(col) * (col + 1) / 2 + (row)];
    } else {
        return (*this)[(row) * (row + 1) / 2 + (col)];
    }
}

const double &SymmetricMatrix::operator()(int row, int col) const {
    if (row >= size() || col >= size()) {
        throw logic_error("index out of bound");
    }
    if (row < col) {
        return (*this)[(col) * (col + 1) / 2 + (row)];
    } else {
        return (*this)[(row) * (row + 1) / 2 + (col)];
    }
}

double SymmetricMatrix::powerIteration(double tau) const {
    if (tau <= 0) {
        throw logic_error("tau may not be smaller than 0.");
    }

    double last_x[size()];
    for (int i{}; i < size(); i++) {
        last_x[i] = 1;
    }

    double x[size()];

    // x = A * last_x
    for (int i{}; i < size(); i++) {
        for (int j{}; j < size(); j++) {
            x[i] += (*this)(i, j) * last_x[j];
        }
    }

    double curr_lambda{0};
    double last_lambda{0};

    while (true) {
        // calculate norm
        double norm{};
        for (int i{}; i < size(); i++) {
            norm += x[i] * x[i];
        }
        norm = sqrt(norm);

        // x = A*last_x / norm
        // last_x = x
        for (int i{}; i < size(); i++) {
            x[i] = x[i] / norm;
            last_x[i] = x[i];
        }

        // x = A * x
        for (int i{}; i < size(); i++) {
            double tmp{};
            for (int j{}; j < size(); j++) {
                tmp += (*this)(i, j) * x[j];
            }
            x[i] = tmp;
        }

        last_lambda = curr_lambda;
        curr_lambda = 0;
        for (int i{}; i < size(); i++) {
            curr_lambda += last_x[i] * x[i];
        }

        // calculate norm of difference of ax and lambda * x
        // diff = (A*last_x) - lambda * last_x
        norm = 0;
        for (int i{}; i < size(); i++) {
            norm += (x[i] - curr_lambda * last_x[i]) * (x[i] - curr_lambda * last_x[i]);
        }
        norm = sqrt(norm);

        if (norm <= tau) {
            if (fabs(curr_lambda) <= tau) {
                if (fabs(last_lambda - curr_lambda) <= tau) {
                    break;
                }
            } else {
                if (fabs(last_lambda - curr_lambda) <= tau * fabs(curr_lambda)) {
                    break;
                }
            }
        }
    }

    return curr_lambda;
}

const LowerTriangularMatrix SymmetricMatrix::computeCholesky() const {
    LowerTriangularMatrix res(size(), 0);

    for (int i{}; i < size(); i++) {
        for (int j{}; j <= i; j++) {
            if (i == j) {
                double tmp{};
                for(int k{}; k < j - 1; k++) {
                    tmp += res(j, k) * res(j, k);
                }

                res(i, i) = sqrt((*this)(i, i) - tmp);
            } else {
                double tmp{};
                for (int k{}; k < j - 1; k++) {
                    tmp += res(i, k) * res(j, k);
                }
                res(i, j) = 1 / res(j, j) * ((*this)(i, j) - tmp);
            }
        }
    }

    return res;
}
