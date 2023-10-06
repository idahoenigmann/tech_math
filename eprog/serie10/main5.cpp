#include <iostream>

#include "Matrix.h"

using namespace std;

int main() {

    {
        cout << "                         _            _____ \n"
                "                        (_)          | ____|\n"
                "   _____  _____ _ __ ___ _ ___  ___  | |__  \n"
                "  / _ \\ \\/ / _ \\ '__/ __| / __|/ _ \\ |___ \\ \n"
                " |  __/>  <  __/ | | (__| \\__ \\  __/  ___) |\n"
                "  \\___/_/\\_\\___|_|  \\___|_|___/\\___| |____/ \n" << endl;

        Matrix matrix(5, -1.6, 42.5);
        matrix.printMatrix();
    }

    return 0;
}