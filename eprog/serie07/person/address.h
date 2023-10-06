//
// Created by ida on 26.11.20.
//

#ifndef EPROG_ADRESS_H
#define EPROG_ADRESS_H

#include <stdlib.h>
#include <string.h>
#include <assert.h>

typedef struct Address_ {
    char* street;
    char* number;
    char* city;
    char* zip;
} Address;

Address* newAddress(char* street, char* number, char* city, char* zip);
Address* delAddress(Address* address);

void setStreet(Address* address, char* street);
void setNumber(Address* address, char* number);
void setCity(Address* address, char* city);
void setZip(Address* address, char* zip);

char* getStreet(Address* address);
char* getNumber(Address* address);
char* getCity(Address* address);
char* getZip(Address* address);

#endif //EPROG_ADRESS_H
