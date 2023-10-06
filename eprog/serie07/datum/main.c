//
// Created by ida on 26.11.20.
//

#include <stdio.h>
#include "datum.h"

int main() {
    Date* date = newDate(27, 11, 2020);

    printf("%d. %d. %d\n", getDateDay(date), getDateMonth(date), getDateYear(date));

    printf("Is valid date: %d\n", isMeaningful(date));

    int d = 0;
    int m = 0;
    int y = 0;

    printf("Please enter a day: ");
    scanf("%d", &d);

    printf("Please enter a month: ");
    scanf("%d", &m);

    printf("Please enter a year: ");
    scanf("%d", &y);

    setDateDay(date, d);
    setDateMonth(date, m);
    setDateYear(date, y);

    printf("%d. %d. %d\n", getDateDay(date), getDateMonth(date), getDateYear(date));

    printf("Is valid date: %d\n", isMeaningful(date));

    date = delDate(date);

    return 0;
}

/* Tested:
 * -1. 10. 2020
 * 1. 1. 1.
 * 1. 1. 1900
 * 29. 2. 2020
 * 29. 2. 2021
 */