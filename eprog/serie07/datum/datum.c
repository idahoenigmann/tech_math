//
// Created by ida on 24.11.20.
//

#include "datum.h"

Date* newDate(int d, int m, int y) {
    Date* date = malloc(sizeof(Date));
    setDateDay(date, d);
    setDateMonth(date, m);
    setDateYear(date, y);
    return date;
}

Date* delDate(Date* date) {
    free(date);
    return NULL;
}

void setDateDay(Date* date, int d) {
    date->day = d;
}

void setDateMonth(Date* date, int m) {
    date->month = m;
}

void setDateYear(Date* date, int y) {
    date->year = y;
}

int getDateDay(Date* date) {
    return date->day;
}

int getDateMonth(Date* date) {
    return date->month;
}

int getDateYear(Date* date) {
    return date->year;
}

int isMeaningful(Date* date) {
    if (date->year < 1900) {
        return 0;
    }
    if (date->month > 12 || date->month < 1) {
        return 0;
    }
    if (date->day < 1) {
        return 0;
    }

    if (date->month == 2) {
        if (date->year % 4 != 0) {
            if (date->day > 28) {
                return 0;
            }
        } else if(date->year % 100 != 0) {
            if (date->day > 29) {
                return 0;
            }
        } else if (date->year % 400 != 0) {
            if (date->day > 28) {
                return 0;
            }
        } else {
            if (date->day > 29) {
                return 0;
            }
        }

    } else if (date->month == 4 || date->month == 6 || date->month == 9 || date->month == 11) {
        if (date->day > 30) {
            return 0;
        }
    } else {
        if (date->day > 31) {
            return 0;
        }
    }
    return 1;
}