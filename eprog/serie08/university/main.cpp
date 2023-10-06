//
// Created by ida on 02.12.20.
//

#include <iostream>

#include "University.h"

using std::cout;
using std::endl;

int main() {
    University tu_wien;
    tu_wien.setName("TU Wien");
    tu_wien.setCity("Wien");
    tu_wien.setNumStudents(5);

    cout << tu_wien.getName() << " - " <<
    tu_wien.getCity() << " : " << tu_wien.getNumStudents() << endl;

    tu_wien.graduate();

    cout << tu_wien.getNumStudents() << endl;

    tu_wien.newStudent();

    cout << tu_wien.getNumStudents() << endl;

    tu_wien.setNumStudents(0);

    //tu_wien.graduate();

    return 0;
}