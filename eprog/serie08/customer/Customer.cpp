//
// Created by ida on 02.12.20.
//

#include "Customer.h"

using std::cout;
using std::endl;
using std::cin;

void Customer::setupAccount(double balance) {
    cout << "Please enter a pin: ";
    cin >> pin;
    this->setBalance(balance);
}

std::string Customer::getName() {
    return name;
}

double Customer::getBalance() {
    return balance;
}

void Customer::setName(std::string new_name) {
    name = new_name;
}

void Customer::setBalance(double new_balance) {
    balance = new_balance;
}

void Customer::setPin(int new_pin) {
    assert(checkPIN());
    pin = new_pin;
}

void Customer::printBalace() {
    cout << balance << endl;
}

bool Customer::checkPIN() {
    cout << "Please enter your pin: ";

    int input_pin;

    cin >> input_pin;
    if (input_pin == pin) {
        return true;
    }
    return false;
}

void Customer::drawMoney(double amount) {
    assert(checkPIN());
    if (amount == 0) {
        cout << "Please enter the amount which should be withdrawn: ";
        cin >> amount;
    }
    assert(amount > 0);
    assert(balance - amount > 0);

    balance -= amount;
    printBalace();
    if (balance < 10) {
        cout << "Warning: you only have fewer than 10 EUR left." << endl;
    }
}