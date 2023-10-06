//
// Created by ida on 09.11.20.
//

#include <stdio.h>

int check(int x[], int y[]) {
    for (int i=0; i < 4; i++) {
        if (x[i] == y[0] && x[i+1] == y[1] && x[i+2] == y[2]) {
            return 1;
        }
    }
    return 0;
}

int main() {
    printf("Checks whether a combination of 3 numbers is contained in the combination of 6 numbers specified.\n");
    int x[6];
    int y[3];

    for (int i=0; i < 6; i++) {
        printf("Please enter a value for x[%d]: ",i);
        scanf("%d",x+i);
    }
    printf("\n");
    for (int i=0; i < 3; i++) {
        printf("Please enter a value for y[%d]: ",i);
        scanf("%d",y+i);
    }
    printf("\n");

    printf("%d\n",check(x,y));

    return 0;
}