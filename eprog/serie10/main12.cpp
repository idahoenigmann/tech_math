#include <iostream>

#include "Matrix.h"

using namespace std;

int main() {

    {
        cout << "                         _            __ \n"
                "                        (_)          /_ |\n"
                "   _____  _____ _ __ ___ _ ___  ___   | |\n"
                "  / _ \\ \\/ / _ \\ '__/ __| / __|/ _ \\  | |\n"
                " |  __/>  <  __/ | | (__| \\__ \\  __/  | |\n"
                "  \\___/_/\\_\\___|_|  \\___|_|___/\\___|  |_|\n" << endl;

        Matrix m1;

        Matrix m2(3);
        cout << "m2[1,2] = " << m2.getCoefficient(1, 2) << endl;

        m2.setCoefficient(42,1,2);
        cout << "m2[1,2] = " << m2.getCoefficient(1, 2) << endl;

        Matrix m3(5, 7);
        cout << "m3[0,0] = " << m3.getCoefficient(0, 0) << endl;

        Matrix m4 = m2;
        cout << "m4[1,2] = " << m4.getCoefficient(1, 2) << endl;

        m4 = m3;
        cout << "m4[1,2] = " << m4.getCoefficient(1, 2) << endl;
    }

    {
        cout << "                         _            ___  \n"
                "                        (_)          |__ \\ \n"
                "   _____  _____ _ __ ___ _ ___  ___     ) |\n"
                "  / _ \\ \\/ / _ \\ '__/ __| / __|/ _ \\   / / \n"
                " |  __/>  <  __/ | | (__| \\__ \\  __/  / /_ \n"
                "  \\___/_/\\_\\___|_|  \\___|_|___/\\___| |____|\n" << endl;

        Matrix m;
        m.scanMatrix(3);
        m.printMatrix();
        cout << m.trace() << endl;
    }

    return 0;
}
