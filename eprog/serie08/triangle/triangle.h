//
// Created by ida on 02.12.20.
//

#ifndef EPROG_TRIANGLE_H
#define EPROG_TRIANGLE_H

#include <cmath>

// The class Triangle stores a triangle in R2

class Triangle {
private:
    double x[2];
    double y[2];
    double z[2];

public:
    // methods to access vertices
    void setX(double, double);
    void setY(double, double);
    void setZ(double, double);
    // method to compute the area of the triangle
    double getArea();
    // method to compute the perimeter of the triangle
    double getPerimeter();
    // checks whether the triangle is equilateral
    bool isEquilateral();
};

#endif //EPROG_TRIANGLE_H
