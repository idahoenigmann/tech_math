//
// Created by ida on 24.10.20.
//

#include <stdio.h>

void hanoi(int m, int i, int j) {
    if (m == 0)
        return;

    // find auxiliary rod
    /*
    int k = 1;
    for (int l=1; l <= 3; l++) {
        if (i != l && j != l) {
            k = l;
            break;
        }
    }
     */

    // i=1; j=2; 1 + 2 = 3 : 3 : 6 - 3
    // i=1; j=3; 1 + 3 = 4 : 2 : 6 - 4
    // i=2; j=3; 2 + 3 = 5 : 1 : 6 - 5

    int k = 6 - (i + j);

    hanoi(m - 1, i, k);
    printf("Move a disk from rod %d to rod %d.\n", i, j);
    hanoi(m - 1, k, j);
}

int main() {
    printf("Solve tower of hanoi problem for n disks.\n");

    int n = 0;
    printf("Please enter a value for n: ");
    scanf("%d", &n);

    hanoi(n, 1, 3);
    return 0;
}