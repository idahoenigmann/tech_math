//
// Created by ida on 02.12.20.
//

#include "Name.h"

using std::cout;
using std::endl;
using std::string;

void Name::setFirstName(std::string new_first_name) {
    first_name = new_first_name;
}

void Name::setSurname(std::string new_surname) {
    surname = new_surname;
}

std::string Name::getFirstName() {
    return first_name;
}

std::string Name::getSurname() {
    return surname;
}

void Name::setFullName(std::string full_name) {
    int idx = full_name.find_last_of(' ');
    first_name = full_name.substr(0, idx);
    surname = full_name.substr(idx + 1, full_name.length() - idx);
}

void Name::printName() {
    int idx = first_name.find(' ');
    cout << first_name.substr(0, idx) << " ";

    while (idx != string::npos) {
        cout << first_name.c_str()[idx + 1] << ". ";
        idx = first_name.find(' ', idx + 1);
    }
    cout << surname << endl;
}