//
// Created by ida on 03.11.20.
//

#include <stdio.h>

void printSudoku(int x[]) {
    printf("-----------------\n");
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            printf("| %d ", x[i*4+j]);
        }
        printf("|\n-----------------\n");
    }
}

int checkUnit(int a, int b, int c, int d) {
    if (a == b || a == c || a == d){
        return 0;
    } else if (b == c || b == d){
        return 0;
    } else if (c == d) {
        return 0;
    } else {
        return 1;
    }
}

void checkSudoku(int x[]) {
    // check rows
    for (int i = 0; i < 4; i++) {
        if (!checkUnit(x[4 * i], x[4 * i + 1], x[4 * i + 2], x[4 * i + 3])) {
            printf("incorrect solution! (tip: row %d)\n", i + 1);
            return;
        }
    }

    // check cols
    for (int i = 0; i < 4; i++) {
        if (!checkUnit(x[i], x[i + 4], x[i + 8], x[i + 12])) {
            printf("incorrect solution! (tip: column %d)\n", i + 1);
            return;
        }
    }

    // check blocks
    int a = 0;
    for (int i = 0; i < 4; i++) {
        if (!checkUnit(x[a], x[a + 1], x[a + 4], x[a + 4 + 1])) {
            printf("incorrect solution! (tip: block %d)\n", i + 1);
            return;
        }
        a += 2;
        if (i + 1 == 4 / 2) {
            a += 4;
        }
    }

    printf("correct solution!\n");
}

int main() {
    int x[16] = {1, 2, 3, 4, 3, 4, 1, 2, 2, 3, 4, 1, 4, 1, 2, 3};   // correct
    // int x[16] = {2, 2, 3, 4, 3, 4, 1, 2, 2, 3, 4, 1, 4, 1, 2, 3};    // error in row
    // int x[16] = {1, 2, 3, 4, 3, 4, 1, 2, 2, 3, 1, 4, 4, 1, 2, 3};    // error in col
    // int x[16] = {1, 2, 4, 3, 4, 1, 3, 2, 3, 4, 2, 1, 2, 3, 1, 4};    // error in block
    printSudoku(x);
    checkSudoku(x);
    return 0;
}

/* Test:
 * using the above test cases.
 */