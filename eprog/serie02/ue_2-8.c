#include <stdio.h>

int main() {
    int x = 1;
    int y = 2;
    int z = 3;

    printf("(%d,%d,%d)\n", x, y, z);

    {
        int x = 100;
        y = 2;
        if (x > y) {
            z = x;
        } else {
            z = y;
        }

        printf("(%d,%d,%d)\n", x, y, z);

        {
            int z = y;
            y = 200;

            printf("(%d,%d,%d)\n", x, y, z);
        }
        printf("(%d,%d,%d)\n", x, y, z);
    }
    printf("(%d,%d,%d)\n", x, y, z);
}