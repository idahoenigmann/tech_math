#include <iostream>

#include "Account.h"
#include "Bank.h"

using namespace std;

int main() {
    Account a;
    SavingsAccount b(5.26, 0.01);
    CurrentAccount c(2.14, 1000);

    cout << a.get_account_number() << endl;
    a.deposit(100);
    a.print();
    a.withdraw(50);
    a.print();

    cout << b.get_account_number() << endl;
    b.deposit(25.4);
    b.print();
    cout << b.get_service_fee() << endl;
    b.chargeFee();
    b.addInterest();
    b.print();

    cout << c.get_account_number() << endl;
    c.deposit(10);
    c.print();
    c.withdraw(500);
    c.print();
    try {
        c.withdraw(800);
    } catch (logic_error& e) {
        cout << e.what() << endl;
    }

    Bank bank;
    bank.addAccount(a);
    bank.addAccount(b);
    bank.addAccount(c);

    bank.updateAccount();

    bank.closeAccount(2);

    b.print();
    c.print();

    return 0;
}