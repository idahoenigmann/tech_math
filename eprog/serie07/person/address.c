//
// Created by ida on 26.11.20.
//

#include "address.h"


Address* newAddress(char* street, char* number, char* city, char* zip) {
    Address* address = malloc(sizeof(Address));

    address->street = malloc(sizeof(char) * (strlen(street) + 1));
    address->number = malloc(sizeof(char) * (strlen(number) + 1));
    address->city = malloc(sizeof(char) * (strlen(city) + 1));
    address->zip = malloc(sizeof(char) * (strlen(zip) + 1));

    setStreet(address, street);
    setNumber(address, number);
    setCity(address, city);
    setZip(address, zip);

    return address;
}

Address* delAddress(Address* address) {
    assert(address != NULL);
    free(address->street);
    free(address->number);
    free(address->city);
    free(address->zip);

    free(address);
    return NULL;
}

void setStreet(Address* address, char* street) {
    address->street = realloc(address->street, sizeof(char) * (strlen(street) + 1));
    strcpy(address->street, street);
}

void setNumber(Address* address, char* number) {
    address->number = realloc(address->number, sizeof(char) * (strlen(number) + 1));
    strcpy(address->number, number);
}

void setCity(Address* address, char* city) {
    address->city = realloc(address->city, sizeof(char) * (strlen(city) + 1));
    strcpy(address->city, city);
}

void setZip(Address* address, char* zip) {
    address->zip = realloc(address->zip, sizeof(char) * (strlen(zip) + 1));
    strcpy(address->zip, zip);
}


char* getStreet(Address* address) {
    char* street;
    street = malloc(sizeof(char) * (strlen(address->street) + 1));
    return street;
}

char* getNumber(Address* address) {
    char* number;
    number = malloc(sizeof(char) * (strlen(address->number) + 1));
    return number;
}

char* getCity(Address* address) {
    char* city;
    city = malloc(sizeof(char) * (strlen(address->city) + 1));
    return city;
}

char* getZip(Address* address) {
    char* zip;
    zip = malloc(sizeof(char) + (strlen(address->zip) + 1));
    return zip;
}