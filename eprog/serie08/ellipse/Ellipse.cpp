//
// Created by ida on 02.12.20.
//

#include "Ellipse.h"

using std::cout;
using std::endl;

double Ellipse::getCenterX() {
    return center[0];
}

double Ellipse::getCenterY() {
    return center[1];
}

double Ellipse::getA() {
    return a;
}

double Ellipse::getB() {
    return b;
}

void Ellipse::setCenterX(double center_x) {
    center[0] = center_x;
}

void Ellipse::setCenterY(double center_y) {
    center[1] = center_y;
}

void Ellipse::setA(double new_a) {
    a = new_a;
}

void Ellipse::setB(double new_b) {
    b = new_b;
}

bool Ellipse::isInside(double x, double y) {
    double accuracy = 0.01;

    double dist_x = (x - center[0]) * (x - center[0]) / a * a;
    double dist_y = (y - center[1]) * (y - center[1]) / b * b;
    if (dist_x + dist_y < 1 - accuracy / 2) {
        return true;
    } else if (dist_x + dist_y - 1 < accuracy) {
        cout << "The point lies on the boundary." << endl;
        return true;
    }
    return false;
}

bool Ellipse::isCircle() {
    double accuracy = 0.01;
    if (fabs(a - b) < accuracy) {
        return true;
    }
    return false;
}

void Ellipse::printFocalPoints() {
    double focal_point1[2];
    double focal_point2[2];
    double c;
    if (this->isCircle()) {
        focal_point1[0] = center[0];
        focal_point1[1] = center[1];
        focal_point2[0] = center[0];
        focal_point2[1] = center[1];
    } else if (a > b) {
        c = sqrt(a * a - b * b);
        focal_point1[0] = center[0] - c;
        focal_point1[1] = center[1];

        focal_point2[0] = center[0] + c;
        focal_point2[1] = center[1];
    } else {
        c = sqrt(b * b - a * a);
        focal_point1[0] = center[0];
        focal_point1[1] = center[1] - c;

        focal_point2[0] = center[0];
        focal_point2[1] = center[1] + c;
    }
    cout << "Focal Points : (" << focal_point1[0] << ", " << focal_point1[1];
    cout << "), (" << focal_point2[0] << ", " << focal_point2[1] << ")" << endl;
}

double Ellipse::getEccentricity() {
    if (a < b) {
        return sqrt(1 - (a / b) * (a / b));
    } else {
        return sqrt(1 - (b / a) * (b / a));
    }
}