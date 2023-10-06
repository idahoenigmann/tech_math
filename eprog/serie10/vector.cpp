#include "vector.hpp"
using std::cout;

Vector::Vector() {
  dim = 0;
  coeff = (double*) 0;
}

Vector::Vector(int dim, double init) {
  assert(dim >= 0);
  this->dim = dim;
  if (dim == 0) {
    coeff = (double*) 0;
  }
  else {
    coeff = new double[dim];
    for (int j=0; j<dim; ++j) {
      coeff[j] = init;
    }
  }
}

Vector::Vector(const Vector& rhs) {
  dim = rhs.dim;
  if (dim == 0) {
    coeff = (double*) 0;
  }
  else {
    coeff = new double[dim];
    for (int j=0; j<dim; ++j) {
      coeff[j] = rhs[j];
    }
  }
}

Vector::~Vector() {
  if (dim > 0) {
    delete[] coeff;
  }
}

Vector& Vector::operator=(const Vector& rhs) {
  if (this != &rhs) {
    if (dim != rhs.dim) {
      if (dim > 0) {
        delete[] coeff;
      }
      dim = rhs.dim;
      if (dim > 0) {
        coeff = new double[dim];
      }
      else {
        coeff = (double*) 0;
      }
    }
    for (int j=0; j<dim; ++j) {
      coeff[j] = rhs[j];
    }
  }
  return *this;
}

int Vector::size() const {
  return dim;
}

const double& Vector::operator[](int k) const {
  assert(k>=0 && k<dim);
  return coeff[k];
}

double& Vector::operator[](int k) {
  assert(k>=0 && k<dim);
  return coeff[k];
}

double Vector::norm() const {
  double sum = 0;
  for (int j=0; j<dim; ++j) {
    sum = sum + coeff[j]*coeff[j];
  }
  return sqrt(sum);
}

std::ostream& operator<<(std::ostream& output,
                         const Vector& x) {
  output << "(";
  for (int j=0; j<x.size(); ++j) {
    output << x[j];
    if ( j < x.size()-1 ) {
      output << ", ";
    }
  }
  return output << ")";
}

const Vector operator+(const Vector& rhs1,
                       const Vector& rhs2) {
  assert(rhs1.size() == rhs2.size());
  Vector result(rhs1);
  for (int j=0; j<result.size(); ++j) {
    result[j] += rhs2[j];
  }
  return result;
}

const Vector operator*(const double scalar,
                       const Vector& input) {
  Vector result(input);
  for (int j=0; j<result.size(); ++j) {
    result[j] *= scalar;
  }
  return result;
}

const Vector operator*(const Vector& input,
                       const double scalar) {
  return scalar*input;
}

const double operator*(const Vector& rhs1,
                       const Vector& rhs2) {
  double scalarproduct = 0;
  assert(rhs1.size() == rhs2.size());
  for (int j=0; j<rhs1.size(); ++j) {
    scalarproduct += rhs1[j]*rhs2[j];
  }
  return scalarproduct;
}
