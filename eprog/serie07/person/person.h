//
// Created by ida on 26.11.20.
//

#ifndef EPROG_PERSON_H
#define EPROG_PERSON_H

#include <assert.h>

#include "../datum/datum.h"
#include "address.h"

typedef struct Person_ {
    char* firstname;
    char* surname;
    Address* address;
    Date* birthday;
} Person;

Person* newPerson(char* firstname, char* surname, Address* address, Date* birthday);
Person* delPerson(Person* person);

void setFirstname(Person* person, char* firstname);
void setSurname(Person* person, char* surname);
void setAddress(Person* person, Address* address);
void setBirthday(Person* person, Date* birthday);

char* getFirstname(Person* person);
char* getSurname(Person* person);
Address* getAddress(Person* person);
Date* getBirthday(Person* person);

Person* whoIsOlder(Person* a, Person* b);

#endif //EPROG_PERSON_H
