//
// Created by ida on 26.11.20.
//

#include <stdio.h>

#include "person.h"

int main() {
    Address* address_donald = newAddress("Webfoot Walk", "1313", "Duckburg", "1234");
    Date* birthday_donald = newDate(9, 6, 1934);

    Person* donald = newPerson("Donald", "Duck", address_donald, birthday_donald);

    Address* address_mickey = newAddress("Rainbow Road", "1A", "Mouse village", "2357");
    Date* birthday_mickey = newDate(1, 1, 1928);

    Person* mickey = newPerson("Mickey", "Mouse", address_mickey, birthday_mickey);

    printf("%s is older.\n",whoIsOlder(mickey, donald)->firstname);

    delPerson(donald);
    delPerson(mickey);
}