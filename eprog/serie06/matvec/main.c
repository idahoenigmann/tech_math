//
// Created by ida on 18.11.20.
//

#include "matvec.h"

int main () {
    double* matrix = mallocMatrix(2, 3);

    printMatrix(matrix, 2, 3);

    matrix = reallocMatrix(matrix, 2, 3, 4, 3);

    matrix = freeMatrix(matrix);

    matrix = scanMatrix(2, 3);

    double* vector = scanVector(3);

    printMatrix(matrix, 2, 3);

    printf("matrix norm: %f\n", matrixNorm(matrix, 2, 3));

    double* product = matrixVectorProduct(matrix, 2, 3, vector, 3);

    printVector(product, 2);

    freeMatrix(product);
    freeVector(vector);
    freeMatrix(matrix);
    return 0;
}
