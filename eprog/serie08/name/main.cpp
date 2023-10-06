//
// Created by ida on 02.12.20.
//

#include <iostream>

#include "Name.h"

using std::cout;
using std::endl;

int main() {
    Name name;
    name.setFirstName("Daisy");
    name.setSurname("Duck");

    cout << name.getFirstName() << " " << name.getSurname() << endl;

    name.setFullName("Donald Fauntleroy Duck");

    cout << "First Name: " << name.getFirstName() << endl;
    cout << "Surname: " << name.getSurname() << endl;

    name.printName();

    name.setFullName("Abc Def Ghi Jkl");
    name.printName();
    return 0;
}