//
// Created by ida on 16.11.20.
//

#include "matvec.h"

double* mallocVector(int n) {
    int j = 0;
    double* vector = NULL;
    assert(n > 0);

    vector = malloc(n*sizeof(double));
    assert(vector != NULL);

    for (j=0; j<n; ++j) {
        vector[j] = 0;
    }
    return vector;
}

double* freeVector(double* vector) {
    free(vector);
    return NULL;
}

double* reallocVector(double* vector, int n, int nnew) {
    int j = 0;
    assert(vector != NULL);
    assert(n > 0);
    assert(nnew > 0);

    vector = realloc(vector,nnew*sizeof(double));
    assert(vector != NULL);
    for (j=n; j<nnew; ++j) {
        vector[j] = 0;
    }
    return vector;
}

double* scanVector(int n) {
    int j = 0;
    double* vector = NULL;
    assert(n > 0);

    vector = mallocVector(n);
    assert(vector != NULL);

    for (j=0; j<n; ++j) {
        printf("vector[%d] = ",j);
        scanf("%lf",&vector[j]);
    }
    return vector;
}

void printVector(double* vector, int n) {
    int j = 0;
    assert(vector != NULL);
    assert(n > 0);

    for (j=0; j<n; ++j) {
        printf("%d: %f\n",j,vector[j]);
    }
}


double* mallocMatrix(int m, int n) {
    int j = 0;
    double* matrix = NULL;
    assert(m > 0);
    assert(n > 0);

    matrix = malloc(m*n*sizeof(double));
    assert(matrix != NULL);

    for (j=0; j<m*n; ++j) {
        matrix[j] = 0;
    }
    return matrix;
}

double* freeMatrix(double* matrix) {
    free(matrix);
    return NULL;
}

/* Remark: does not work as expected, because the original values do not match the new ones. */
double* reallocMatrix(double* matrix, int m, int n, int mnew, int nnew) {
    int j = 0;
    assert(matrix != NULL);
    assert(m > 0);
    assert(n > 0);
    assert(mnew > 0);
    assert(nnew > 0);

    matrix = realloc(matrix,mnew*nnew*sizeof(double));
    assert(matrix != NULL);
    for (j=n; j<mnew*nnew; ++j) {
        matrix[j] = 0;
    }
    return matrix;
}

double* scanMatrix(int m, int n) {
    int i = 0;
    int j = 0;
    double* matrix = NULL;
    assert(m > 0);
    assert(n > 0);

    matrix = mallocMatrix(m, n);
    assert(matrix != NULL);

    for (i=0; i<m; ++i) {
        for (j=0; j<n; ++j) {
            printf("matrix[%d, %d] = ",i, j);
            scanf("%lf",&matrix[i+j*m]);
        }
    }

    return matrix;
}

void printMatrix(double* matrix, int m, int n) {
    int i = 0;
    int j = 0;
    assert(matrix != NULL);
    assert(m > 0);
    assert(n > 0);

    for (i=0; i<m; ++i) {
        for (j = 0; j < n; ++j) {
            printf("%d, %d: %f\n", i, j, matrix[j*m+i]);
        }
    }
}

double* matrixVectorProduct(double* matrix, int mMat, int nMat, double* vector, int nVec) {
    assert(nMat == nVec);

    double* res;

    res = mallocVector(mMat);

    for (int i=0; i < mMat; i++) {
        double sum = 0;
        for (int j=0; j < nMat; j++) {
            sum += matrix[i+j*mMat]*vector[j];
        }
        res[i] = sum;
    }
    return res;
}

double matrixNorm(double* matrix, int m, int n) {
    double res = 0;

    for (int i=0; i < m; i++) {
        for (int j=0; j < n; j++) {
            res += matrix[j*m+i] * matrix[j*m+i];
        }
    }

    return sqrt(res);
}