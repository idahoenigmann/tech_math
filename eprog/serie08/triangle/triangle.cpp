//
// Created by ida on 02.12.20.
//

#include "triangle.h"

void Triangle::setX(double x0, double x1) {
    x[0] = x0;
    x[1] = x1;
}

void Triangle::setY(double y0, double y1) {
    y[0] = y0;
    y[1] = y1;
}

void Triangle::setZ(double z0, double z1) {
    z[0] = z0;
    z[1] = z1;
}

double Triangle::getArea() {
    // use the 2x2 determinant formula to compute the area
    return 0.5*fabs( (y[0]-x[0])*(z[1]-x[1])
                     - (z[0]-x[0])*(y[1]-x[1]) );
}

double Triangle::getPerimeter() {
    // length between point x and y
    double len_a = sqrt((x[0] - y[0]) * (x[0] - y[0]) +
            (x[1] - y[1]) * (x[1] - y[1]));
    // length between point y and z
    double len_b = sqrt((y[0] - z[0]) * (y[0] - z[0]) +
                        (y[1] - z[1]) * (y[1] - z[1]));
    // length between point z and x
    double len_c = sqrt((z[0] - x[0]) * (z[0] - x[0]) +
                        (z[1] - x[1]) * (z[1] - x[1]));
    return len_a + len_b + len_c;
}

bool Triangle::isEquilateral() {
    double accuracy = 0.01;
    // length between point x and y
    double len_a = sqrt((x[0] - y[0]) * (x[0] - y[0]) +
                        (x[1] - y[1]) * (x[1] - y[1]));
    // length between point y and z
    double len_b = sqrt((y[0] - z[0]) * (y[0] - z[0]) +
                        (y[1] - z[1]) * (y[1] - z[1]));
    // length between point z and x
    double len_c = sqrt((z[0] - x[0]) * (z[0] - x[0]) +
                        (z[1] - x[1]) * (z[1] - x[1]));
    if (fabs(len_a - len_b) < accuracy && fabs(len_b - len_c) < accuracy) {
        return true;
    }
    return false;
}