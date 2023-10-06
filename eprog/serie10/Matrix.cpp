//
// Created by ida on 16.12.20.
//

#include "Matrix.h"

using namespace std;

double Matrix::getCoefficient(unsigned int row, unsigned int col) const{
    if (row >= dim || col >= dim) {
        throw logic_error("Index out of bounds.");
    }

    return coeff[col*dim+row];
}

void Matrix::setCoefficient(double num, unsigned int row, unsigned int col) {
    if (row >= dim || col >= dim) {
        throw logic_error("Index out of bounds.");
    }

    this->coeff[col*dim+row] = num;
}

Matrix::Matrix(unsigned int dimension, double coeff) {
    dim = dimension;
    this->coeff = new double[dim*dim];

    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            setCoefficient(coeff, i, j);
        }
    }
}

Matrix::~Matrix() {
    delete[] coeff;
}

Matrix::Matrix(const Matrix &matrix) {
    dim = matrix.dim;
    coeff = new double[dim*dim];

    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            setCoefficient(matrix.getCoefficient(i, j), i, j);
        }
    }
}

Matrix &Matrix::operator=(const Matrix &matrix) {
    if (this == &matrix) {
        return *this;
    }

    if (matrix.dim != dim) {
        dim = matrix.dim;
        delete[] coeff;
        coeff = new double[matrix.dim * matrix.dim];
    }

    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            setCoefficient(matrix.getCoefficient(i, j), i, j);
        }
    }

    return *this;
}

void Matrix::scanMatrix(int dim) {
    if (this->dim != dim) {
        delete [] coeff;
        this->dim = dim;
        coeff = new double[dim * dim];
    }

    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            double number {0};

            cout << "m[" << i << "," << j << "] = " << flush;
            cin >> number;

            setCoefficient(number, i, j);
        }
    }
}

void Matrix::printMatrix() const {
    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            cout << getCoefficient(i, j) << " | ";
        }
        cout << endl;
    }
}

double Matrix::trace() const {
    double sum{0};

    for (int i{0}; i < dim; i++) {
        sum += getCoefficient(i, i);
    }

    return sum;
}

double Matrix::maximumAbsoluteColumnSumNorm() const {
    double max{0};

    double sum{0};
    for (int j{0}; j < dim; j++) {
        sum += getCoefficient(j, 0);
    }

    for(int k{1}; k < dim; k++) {
        sum = 0;
        for (int j{0}; j < dim; j++) {
            sum += fabs(getCoefficient(j, k));
        }
        if (sum > max) {
            max = sum;
        }
    }

    return max;
}

double Matrix::maximumAbsoluteRowSumNorm() const {
    double max{0};

    double sum{0};
    for (int k{0}; k < dim; k++) {
        sum += getCoefficient(0, k);
    }

    for(int j{1}; j < dim; j++) {
        sum = 0;
        for (int k{0}; k < dim; k++) {
            sum += fabs(getCoefficient(j, k));
        }
        if (sum > max) {
            max = sum;
        }
    }

    return max;
}

double Matrix::frobeniusNorm() const {
    double sum{0};

    for (int j{0}; j < dim; j++) {
        for (int k{0}; k < dim; k++) {
            sum += getCoefficient(j, k) * getCoefficient(j, k);
        }
    }

    return sqrt(sum);
}

double Matrix::maxNorm() const {
    double max{fabs(getCoefficient(0, 0))};

    for (int j{0}; j < dim; j++) {
        for (int k{0}; k < dim; k++) {
            if (fabs(getCoefficient(j, k)) > max) {
                max = fabs(getCoefficient(j, k));
            }
        }
    }

    return max;
}

/* Computational complexity of norms: n^2 */

bool Matrix::isDiagonal() const {
    for (int i{0}; i < dim; i++) {
        for (int j{0}; j < dim; j++) {
            if (i == j) {
                continue;
            }
            if (getCoefficient(i, j) != 0) {
                return false;
            }
        }
    }
    return true;
}

bool Matrix::isSymmetric() const {
    for (int i{0}; i < dim; i++) {
        for (int j{0}; j < dim; j++) {
            if (getCoefficient(i, j) != getCoefficient(j, i)) {
                return false;
            }
        }
    }
    return true;
}

bool Matrix::isSkewSymmetric() const {
    for (int i{0}; i < dim; i++) {
        for (int j{0}; j < dim; j++) {
            if (getCoefficient(i, j) != -(getCoefficient(j, i))) {
                return false;
            }
        }
    }
    return true;
}

bool Matrix::isUpperTriangular() const {
    for (int i{0}; i < dim; i++) {
        for (int j{i + 1}; j < dim; j++) {
            if (getCoefficient(j, i) != 0) {
                return false;
            }
        }
    }
    return true;
}

bool Matrix::isLowerTriangular() const {
    for (int i{0}; i < dim; i++) {
        for (int j{0}; j < i; j++) {
            if (getCoefficient(j, i) != 0) {
                return false;
            }
        }
    }
    return true;
}

Matrix::Matrix(unsigned int dimension, double lower_bound, double upper_bound) {
    dim = dimension;
    this->coeff = new double[dim*dim];

    srand(time(NULL));

    for (unsigned int i{0}; i < dim; i++) {
        for (unsigned int j{0}; j < dim; j++) {
            double value = (upper_bound - lower_bound) * ((double)rand() / RAND_MAX) + lower_bound;

            setCoefficient(value, i, j);
        }
    }
}

unsigned int Matrix::getDimension() const{
    return dim;
}
