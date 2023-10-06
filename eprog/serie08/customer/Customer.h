//
// Created by ida on 02.12.20.
//

#ifndef EPROG_CUSTOMER_H
#define EPROG_CUSTOMER_H

#include <iostream>
#include <cassert>
#include <string>

class Customer {
public:
    void setupAccount(double balance);

    std::string getName();
    double getBalance();

    void setName(std::string);

    void printBalace();
    bool checkPIN();
    void drawMoney(double amount = 0);
private:
    std::string name;
    double balance;
    int pin;

    void setBalance(double);
    void setPin(int);
};


#endif //EPROG_CUSTOMER_H
