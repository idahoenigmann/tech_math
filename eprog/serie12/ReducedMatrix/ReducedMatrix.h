//
// Created by ida on 14.01.21.
//

#ifndef SERIE12_REDUCEDMATRIX_H
#define SERIE12_REDUCEDMATRIX_H

#include <stdexcept>
#include <iostream>
#include <math.h>

class ReducedMatrix {
public:
    ReducedMatrix() {
        std::cout << "hello" << std::endl;
    };
    ReducedMatrix(unsigned int coeffLen, double value=0);
    ReducedMatrix(const ReducedMatrix&);
    virtual ~ReducedMatrix();
    virtual ReducedMatrix& operator=(const ReducedMatrix& rhs);
    int size() const;

    virtual double& operator()(int row, int col) = 0;
    virtual const double& operator()(int row, int col) const = 0;

protected:
    virtual const double& operator[](int idx) const;
    virtual double& operator[](int idx);

private:
    unsigned int coeff_len{};
    double* coeff{nullptr};
};

class LowerTriangularMatrix : public ReducedMatrix {
public:
    LowerTriangularMatrix() : ReducedMatrix() {};
    LowerTriangularMatrix(unsigned int coeffLen, double value=0): ReducedMatrix(coeffLen, value) {};
    LowerTriangularMatrix(const LowerTriangularMatrix& rhs) : ReducedMatrix(rhs) {};

    double& operator()(int row, int col) override;
    const double& operator()(int row, int col) const override;
private:
    double zero{0};
    const double const_zero{0};
};

class SymmetricMatrix : public ReducedMatrix {
public:
    SymmetricMatrix() : ReducedMatrix() {};
    SymmetricMatrix(unsigned int coeffLen, double value=0): ReducedMatrix(coeffLen, value) {};
    SymmetricMatrix(const SymmetricMatrix& rhs) : ReducedMatrix(rhs) {};

    double& operator()(int row, int col) override;
    const double& operator()(int row, int col) const override;

    double powerIteration(double tau) const;
    const LowerTriangularMatrix computeCholesky() const;
};

#endif //SERIE12_REDUCEDMATRIX_H
