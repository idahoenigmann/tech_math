//
// Created by ida on 02.12.20.
//

#include <iostream>
#include "Ellipse.h"

using std::cout;
using std::endl;
using std::boolalpha;

int main() {
    Ellipse ellipse;
    ellipse.setCenterX(5);
    ellipse.setCenterY(10);
    ellipse.setA(2);
    ellipse.setB(1);

    cout << boolalpha;

    cout << "Is Inside: " << ellipse.isInside(6, 10) << endl;
    cout << "Is Inside: " << ellipse.isInside(6, 11) << endl;
    cout << "Is Circle: " << ellipse.isCircle() << endl;
    ellipse.printFocalPoints();
    cout << "Get Eccentricity: " << ellipse.getEccentricity() << endl;

    ellipse.setB(2);
    cout << "Is Circle: " << ellipse.isCircle() << endl;
    cout << "Get Eccentricity: " << ellipse.getEccentricity() << endl;

    return 0;
}