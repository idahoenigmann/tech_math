//
// Created by ida on 16.11.20.
//

#ifndef EPROG_MATVEC_H
#define EPROG_MATVEC_H

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>

// allocate + initialize dynamic double vector of length n
double* mallocVector(int n);

// free a dynamic vector and set the pointer to NULL
double* freeVector(double* vector);

// extend dynamic double vector and initialize new entries
double* reallocVector(double* vector, int n, int nnew);

// allocate dynamic double vector of length n and read
// entries from keyboard
double* scanVector(int n);

// print dynamic double vector of length n to shell
void printVector(double* vector, int n);


// allocate + initialize dynamic double matrix of length mxn
double* mallocMatrix(int m, int n);

// free a dynamic matrix and set the pointer to NULL
double* freeMatrix(double* matrix);

// extend dynamic double matrix and initialize new entries
double* reallocMatrix(double* matrix, int m, int n, int mnew, int nnew);

// allocate dynamic double matrix of length mxn and read
// entries from keyboard
double* scanMatrix(int m, int n);

// print dynamic double matrix of length mxn to shell
void printMatrix(double* matrix, int m, int n);


double* matrixVectorProduct(double* matrix, int mMat, int nMat, double* vector, int nVec);

double matrixNorm(double* matrix, int m, int n);

#endif //EPROG_MATVEC_H
