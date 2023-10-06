//
// Created by ida on 02.12.20.
//

#include <iostream>
#include "triangle.h"

using std::cout;
using std::endl;
using std::boolalpha;
using std::noboolalpha;

int main() {
    Triangle triangle;
    triangle.setX(0.0, 0.0);
    triangle.setY(1.0, 0.0);
    triangle.setZ(0.5, 0.866);

    cout << "Triangle perimeter: " << triangle.getPerimeter() << endl;
    cout << "Is triangle equilateral: " << boolalpha << triangle.isEquilateral() << noboolalpha << endl;
    return 0;
}