#include <iostream>

#include "Matrix.h"

using namespace std;

int main() {

    Matrix m;
    m.scanMatrix(3);
    m.printMatrix();

    {
        cout << "                         _            ____  \n"
                "                        (_)          |___ \\ \n"
                "   _____  _____ _ __ ___ _ ___  ___    __) |\n"
                "  / _ \\ \\/ / _ \\ '__/ __| / __|/ _ \\  |__ < \n"
                " |  __/>  <  __/ | | (__| \\__ \\  __/  ___) |\n"
                "  \\___/_/\\_\\___|_|  \\___|_|___/\\___| |____/ \n" << endl;

        cout << "maximumAbsoluteColumnSumNorm = " << m.maximumAbsoluteColumnSumNorm() << endl;
        cout << "maximumAbsoluteRowSumNorm = " << m.maximumAbsoluteRowSumNorm() << endl;
        cout << "frobeniusNorm = " << m.frobeniusNorm() << endl;
        cout << "maxNorm = " << m.maxNorm() << endl;
    }

    {
        cout << "                         _            _  _   \n"
                "                        (_)          | || |  \n"
                "   _____  _____ _ __ ___ _ ___  ___  | || |_ \n"
                "  / _ \\ \\/ / _ \\ '__/ __| / __|/ _ \\ |__   _|\n"
                " |  __/>  <  __/ | | (__| \\__ \\  __/    | |  \n"
                "  \\___/_/\\_\\___|_|  \\___|_|___/\\___|    |_|  \n" << endl;

        cout << "isDiagonal = " << m.isDiagonal() << endl;
        cout << "isSymmetric = " << m.isSymmetric() << endl;
        cout << "isSkewSymmetric = " << m.isSkewSymmetric() << endl;
        cout << "isUpperTriangular = " << m.isUpperTriangular() << endl;
        cout << "isLowerTriangular = " << m.isLowerTriangular() << endl;
    }

    return 0;
}