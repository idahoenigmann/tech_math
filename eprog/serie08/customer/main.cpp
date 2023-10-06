//
// Created by ida on 02.12.20.
//

#include <iostream>

#include "Customer.h"

using std::cout;
using std::endl;
using std::cin;
using std::string;

int main() {
    Customer customer;
    customer.setName("Donald Duck");
    customer.setupAccount(25.02);

    cout << customer.getName() << ": " << customer.getBalance() << endl;

    customer.drawMoney(5);
    customer.drawMoney();
}