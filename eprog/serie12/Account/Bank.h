//
// Created by ida on 13.01.21.
//

#ifndef SERIE12_BANK_H
#define SERIE12_BANK_H

#include <vector>
#include <memory>
#include "Account.h"

class Bank {
public:
    Bank() = default;
    ~Bank() = default;

    void addAccount(Account& account);
    void closeAccount(int account_number);
    void updateAccount();
private:
    std::vector<Account*> accounts;
};


#endif //SERIE12_BANK_H
