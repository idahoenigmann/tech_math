//
// Created by ida on 24.11.20.
//

#include <stdio.h>

int cntChar(char* string, char c) {
    int idx = 0;
    int res = 0;
    while (string[idx] != '\0') {
        if (string[idx] == c) {
            res++;
        }
        idx++;
    }
    return res;
}

void toLowercase(char* string, char* resString) {
    int idx = 0;
    while (string[idx] != '\0') {
        if (65 <= string[idx] && string[idx] <= 90) {
            resString[idx] = string[idx] + (97 - 65);     // difference between a and A in ascii table
        } else {
            resString [idx] = string[idx];
        }
        idx++;
    }
    resString[idx] = '\0';
}

int anagram(char* firstStr, char* secondStr) {
    char lFirstStr[256];
    char lSecondStr[256];
    toLowercase(firstStr, lFirstStr);
    toLowercase(secondStr, lSecondStr);

    int idx = 0;
    while (lFirstStr[idx] != '\0' && lSecondStr[idx] != '\0') {
        if (cntChar(lFirstStr, lFirstStr[idx]) != cntChar(lSecondStr, lFirstStr[idx])) {
            return 0;
        }
        idx++;
    }
    if (lFirstStr[idx] != '\0' || lSecondStr[idx] != '\0') {
        return 0;
    }
    return 1;
}

int main() {
    printf("Checks two strings for anagram.\n");

    char str_1[256];
    char str_2[256];

    printf("Please enter the first string: ");
    scanf("%s", str_1);

    printf("Please enter the second string: ");
    scanf("%s", str_2);

    if (anagram(str_1, str_2)) {
        printf("The two strings are anagrams of each other.\n");
    } else {
        printf("No anagram. :-(\n");
    }

    return 0;
}

/* Tested:
 * abC, Acb
 * Elvis, lives
 * asdf-jkl, ad-jlkfs
 * abc, def
 * abcdef, def
 * abc, abcdef
 */