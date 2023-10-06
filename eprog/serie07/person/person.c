//
// Created by ida on 26.11.20.
//

#include "person.h"

Person* newPerson(char* firstname, char* surname, Address* address, Date* birthday) {
    Person* person = malloc(sizeof(Person));

    person->firstname = malloc(sizeof(char) * (strlen(firstname) + 1));
    person->surname = malloc(sizeof(char) * (strlen(surname) + 1));
    person->address = malloc(sizeof(Address));
    person->birthday = malloc(sizeof(Date));

    setFirstname(person, firstname);
    setSurname(person, surname);
    setAddress(person, address);
    setBirthday(person, birthday);

    return person;
}

Person* delPerson(Person* person) {
    assert(person != NULL);

    free(person->firstname);
    free(person->surname);
    person->address = delAddress(person->address);
    person->birthday = delDate(person->birthday);

    free(person);
    return NULL;
}

void setFirstname(Person* person, char* firstname) {
    person->firstname = realloc(person->firstname, sizeof(char) * (strlen(firstname) + 1));

    person->firstname = strcpy(person->firstname, firstname);
}

void setSurname(Person* person, char* surname) {
    person->surname = realloc(person->surname, sizeof(char) * (strlen(surname) + 1));

    person->surname = strcpy(person->surname, surname);
}

void setAddress(Person* person, Address* address) {
    person->address->street = address->street;
    person->address->number = address->number;
    person->address->city = address->city;
    person->address->zip = address->zip;
}

void setBirthday(Person* person, Date* birthday) {
    person->birthday->day = birthday->day;
    person->birthday->month = birthday->month;
    person->birthday->year = birthday->year;
}

char* getFirstname(Person* person){
    char* res;
    res = malloc(sizeof(char) * (strlen(person->firstname) + 1));
    strcpy(res, person->firstname);
    return res;
}

char* getSurname(Person* person) {
    char* res;
    res = malloc(sizeof(char) * (strlen(person->surname) + 1));
    strcpy(res, person->surname);
    return res;
}

Address* getAddress(Person* person) {
    Address* res;
    res = malloc(sizeof(Address));
    res->city = person->address->city;
    res->number = person->address->number;
    res->street = person->address->street;
    res->zip = person->address->zip;
    return res;
}

Date* getBirthday(Person* person) {
    Date* res;
    res = malloc(sizeof(Date));
    res->day = person->birthday->day;
    res->month = person->birthday->month;
    res->year = person->birthday->year;
    return res;
}

Person* whoIsOlder(Person* a, Person* b) {
    if (a->birthday->year < b->birthday->year) {
        return a;
    } else if (a->birthday->year > b->birthday->year) {
        return b;
    } else {
        if (a->birthday->month < b->birthday->month) {
            return a;
        } else if (a->birthday->month > b->birthday->month) {
            return b;
        } else {
            if (a->birthday->day < b->birthday->day) {
                return a;
            } else if (a->birthday->day > b->birthday->day) {
                return b;
            } else {    // if both persons share their birthday person a is returned.
                return a;
            }
        }
    }
}