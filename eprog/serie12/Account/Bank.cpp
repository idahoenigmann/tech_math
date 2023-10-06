//
// Created by ida on 13.01.21.
//

#include "Bank.h"

using namespace std;

void Bank::updateAccount() {
    for (int i{0}; i < accounts.size(); i++) {
        accounts.at(i)->update();
    }
}

void Bank::addAccount(Account& account) {
    accounts.push_back(&account);
}

void Bank::closeAccount(int account_number) {
    for (int i{(int)accounts.size() - 1}; i >= 0; i--) {
        if (accounts.at(i)->get_account_number() == account_number) {
            accounts.erase(accounts.begin() + i);
        }
    }
}
