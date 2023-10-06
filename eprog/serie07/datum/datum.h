//
// Created by ida on 24.11.20.
//

#ifndef EPROG_DATUM_H
#define EPROG_DATUM_H

#include <stdlib.h>

typedef struct _Date_ {
    int day;
    int month;
    int year;
} Date;

Date* newDate(int d, int m, int y);

Date* delDate(Date* date);

void setDateDay(Date* date, int d);

void setDateMonth(Date* date, int m);

void setDateYear(Date* date, int y);

int getDateDay(Date* date);

int getDateMonth(Date* date);

int getDateYear(Date* date);

int isMeaningful(Date* date);

#endif //EPROG_DATUM_H
