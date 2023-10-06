#include <iostream>

#include "utils.h"
#include "IntVector.h"
#include "Factorization.h"
#include "Fraction.h"

using namespace std;

int main() {
    cout << "  ______                   _            __     \n"
            " |  ____|                 (_)          /_ |  _ \n"
            " | |__  __  _____ _ __ ___ _ ___  ___   | | (_)\n"
            " |  __| \\ \\/ / _ \\ '__/ __| / __|/ _ \\  | |    \n"
            " | |____ >  <  __/ | | (__| \\__ \\  __/  | |  _ \n"
            " |______/_/\\_\\___|_|  \\___|_|___/\\___|  |_| (_)\n" << endl;

    {
        IntVector vector;
        cout << vector.getLength() << endl;
        try {
            vector.setCoefficient(0, 1);
        } catch (logic_error &error) {
            cout << error.what() << endl;
        }
    }

    {
        IntVector vector = IntVector((unsigned int) 3, 42);
        cout << vector.getLength() << endl;
        cout << vector.getCoefficient(0) << ", ";
        cout << vector.getCoefficient(1) << ", ";
        cout << vector.getCoefficient(2) << endl;
        try {
            cout << vector.getCoefficient(3) << endl;
        } catch (logic_error &error) {
            cout << error.what() << endl;
        }
    }

    cout << "  ______                   _            ___      \n"
            " |  ____|                 (_)          |__ \\   _ \n"
            " | |__  __  _____ _ __ ___ _ ___  ___     ) | (_)\n"
            " |  __| \\ \\/ / _ \\ '__/ __| / __|/ _ \\   / /     \n"
            " | |____ >  <  __/ | | (__| \\__ \\  __/  / /_   _ \n"
            " |______/_/\\_\\___|_|  \\___|_|___/\\___| |____| (_)\n" << endl;

    {
        IntVector vector = IntVector(42);
        cout << "prime numbers <= 42: ";
        for (int i = 0; i < (int)vector.getLength(); i++) {
            cout << vector.getCoefficient(i) << ", ";
        }
        cout << endl;
    }

    cout << "  ______                   _            ____      \n"
            " |  ____|                 (_)          |___ \\   _ \n"
            " | |__  __  _____ _ __ ___ _ ___  ___    __) | (_)\n"
            " |  __| \\ \\/ / _ \\ '__/ __| / __|/ _ \\  |__ <     \n"
            " | |____ >  <  __/ | | (__| \\__ \\  __/  ___) |  _ \n"
            " |______/_/\\_\\___|_|  \\___|_|___/\\___| |____/  (_)\n" << endl;

    {
        Factorization factorization = Factorization(8);
        cout << factorization.recomposeInteger() << endl;
        factorization.setNumber(42);
        cout << factorization.recomposeInteger() << endl;
    }

    cout << "  ______                   _            _  _       \n"
            " |  ____|                 (_)          | || |    _ \n"
            " | |__  __  _____ _ __ ___ _ ___  ___  | || |_  (_)\n"
            " |  __| \\ \\/ / _ \\ '__/ __| / __|/ _ \\ |__   _|    \n"
            " | |____ >  <  __/ | | (__| \\__ \\  __/    | |    _ \n"
            " |______/_/\\_\\___|_|  \\___|_|___/\\___|    |_|   (_)\n" << endl;

    {
        cout << gcd(20, 10) << endl;
        cout << gcd(42, 5) << endl;

        cout << lcm(8 * 3, 8 * 5) << endl;
    }

    cout << "  ______                   _            _____       __    __        __  ______     \n"
            " |  ____|                 (_)          | ____|     / /   / /       / / |____  |  _ \n"
            " | |__  __  _____ _ __ ___ _ ___  ___  | |__      / /   / /_      / /      / /  (_)\n"
            " |  __| \\ \\/ / _ \\ '__/ __| / __|/ _ \\ |___ \\    / /   | '_ \\    / /      / /      \n"
            " | |____ >  <  __/ | | (__| \\__ \\  __/  ___) |  / /    | (_) |  / /      / /     _ \n"
            " |______/_/\\_\\___|_|  \\___|_|___/\\___| |____/  /_/      \\___/  /_/      /_/     (_)\n" << endl;

    {
        Fraction a = Fraction(20, 10);
        cout << a.getNumerator() << "/" << a.getDenominator() << endl;
        a.reduce();
        cout << a.getNumerator() << "/" << a.getDenominator() << " + ";

        Fraction b = Fraction(4, 6);
        cout << b.getNumerator() << "/" << b.getDenominator() << " = ";

        Fraction res = addFractions(a, b);
        cout << res.getNumerator() << "/" << res.getDenominator() << endl;

    }

    return 0;
}
