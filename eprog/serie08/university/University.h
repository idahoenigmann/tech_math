//
// Created by ida on 02.12.20.
//

#ifndef EPROG_UNIVERSITY_H
#define EPROG_UNIVERSITY_H

#include <string>
#include <cassert>

class University {
public:
    std::string getName();
    std::string getCity();
    unsigned int getNumStudents();

    void setName(std::string);
    void setCity(std::string);
    void setNumStudents(unsigned int);

    void graduate();
    void newStudent();

private:
    std::string name;
    std::string city;
    unsigned int num_students;
};


#endif //EPROG_UNIVERSITY_H
