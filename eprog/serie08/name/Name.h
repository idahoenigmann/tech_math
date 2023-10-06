//
// Created by ida on 02.12.20.
//

#ifndef EPROG_NAME_H
#define EPROG_NAME_H

#include <string>
#include <iostream>

class Name {
public:
    void setFirstName(std::string);
    void setSurname(std::string);
    std::string getFirstName();
    std::string getSurname();

    void setFullName(std::string full_name);
    void printName();
private:
    std::string first_name;
    std::string surname;
};


#endif //EPROG_NAME_H
