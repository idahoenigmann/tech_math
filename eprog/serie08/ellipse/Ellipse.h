//
// Created by ida on 02.12.20.
//

#ifndef EPROG_ELLIPSE_H
#define EPROG_ELLIPSE_H

#include <cmath>
#include <iostream>

class Ellipse {
public:
    double getCenterX();
    double getCenterY();
    double getA();
    double getB();

    void setCenterX(double);
    void setCenterY(double);
    void setA(double);
    void setB(double);

    bool isInside(double x, double y);
    bool isCircle();
    void printFocalPoints();
    double getEccentricity();

private:
    double center[2];
    double a;
    double b;
};


#endif //EPROG_ELLIPSE_H
