#include <iostream>

#include "Matrix.h"
#include "vector.hpp"

using namespace std;

Vector solveU(const Matrix& U, const Vector& b) {
    if (!U.isUpperTriangular()) {
        throw logic_error("Matrix has to be upper triangular.");
    }
    if (U.getDimension() != b.size()) {
        throw logic_error("Matrix size does not match Vector size.");
    }

    for (int i{0}; i < b.size(); i++) {
        if (U.getCoefficient(i, i) == 0) {
            throw logic_error("The diagonal can't have 0 entries.");
        }
    }

    Vector res(b.size());

    for (int i{b.size() - 1}; i >= 0; i--) {
        double tmp{b[i]};

        for (int j{i}; j < b.size(); j++) {
            tmp -= U.getCoefficient(i,j) * res[j];
        }

        res[i] = tmp / U.getCoefficient(i, i);
    }
    return res;
}

/* computational complexity: O(n^2) */

Vector solve(Matrix A, Vector b) {
    if (A.getDimension() != b.size()) {
        throw logic_error("Matrix size does not match Vector size.");
    }

    for (int i{(int)A.getDimension() - 2}; i >= 0; i--) {
        for (int k{(int)A.getDimension() - i - 1}; k > 0; k--) {
            // Subtract k-th col to the right from current col
            double factor{A.getCoefficient(i + k, i) / A.getCoefficient(i + k, i + k)};

            for (int j{0}; j < A.getDimension(); j++) {
                A.setCoefficient(A.getCoefficient(j, i) - A.getCoefficient(j, i+k) * factor, j, i);
            }
        }
    }

    return solveU(A, b);
}

Vector solve2(Matrix A, Vector b) {

    while(true) {
        try {
            return solve(A, b);
        } catch (logic_error &error) {
            // find col with A(x, x) == 0
            int x{0};
            for (; x < A.getDimension(); x++) {
                if (A.getCoefficient(x, x) == 0) {
                    break;
                }
            }

            // find swap col
            int swap_idx{0};
            for (int i{0}; i < A.getDimension(); i++) {
                if (fabs(A.getCoefficient(i, x)) > fabs(A.getCoefficient(swap_idx, x))) {
                    swap_idx = i;
                }
            }
            if (A.getCoefficient(swap_idx, x) == 0) {
                throw logic_error("Pivoting does not work, as the values in a col are all 0.");
            }

            for (int i{0}; i < A.getDimension(); i++) {
                double tmp{A.getCoefficient(i, swap_idx)};
                A.setCoefficient(A.getCoefficient(i, x), i, swap_idx);
                A.setCoefficient(tmp, i, x);
            }
        }
    }

}


int main() {

    {
       Matrix matrix;
       //matrix.scanMatrix(3);

       Vector vector(3);
       vector[0] = 3;
       vector[1] = 2;
       vector[2] = 1;

       try {
           Vector res{solveU(matrix, vector)};

           for (int i{0}; i < 3; i++) {
               cout << res[i] << ", ";
           }
           cout << endl;
       } catch (logic_error &e) {
            cout << e.what() << endl;
       }

    }

    {
        Matrix matrix;
        matrix.scanMatrix(2);

        Vector vector(2);
        vector[0] = 3;
        vector[1] = 4;

        try {
            Vector res{solve2(matrix, vector)};

            for (int i{0}; i < 2; i++) {
                cout << res[i] << ", ";
            }
            cout << endl;
        } catch (logic_error &e) {
            cout << e.what() << endl;
        }
    }

    return 0;
}