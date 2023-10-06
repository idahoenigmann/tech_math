//
// Created by ida on 02.12.20.
//

#include "University.h"

std::string University::getName() {
    return name;
}

std::string University::getCity() {
    return city;
}

unsigned int University::getNumStudents() {
    return num_students;
}

void University::setName(std::string new_name) {
    name = new_name;
}

void University::setCity(std::string new_city) {
    city = new_city;
}

void University::setNumStudents(unsigned int new_num_students) {
    num_students = new_num_students;
}

void University::graduate() {
    assert(num_students > 0);
    num_students--;
}

void University::newStudent() {
    num_students++;
}