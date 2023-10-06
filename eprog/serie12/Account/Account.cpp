//
// Created by ida on 13.01.21.
//

#include "Account.h"

using namespace std;

int Account::next_account_number = 1;

Account::Account(double service_fee) {
    this->account_number = next_account_number;
    next_account_number++;
    this->service_fee = service_fee;
}

Account::Account() {
    this->account_number = next_account_number;
    next_account_number++;
}

int Account::get_account_number() const {
    return account_number;
}

double Account::get_service_fee() const {
    return service_fee;
}

void Account::deposit(double sum) {
    if (sum <= 0) {
        throw logic_error("can not deposit negative amount of cash.");
    }
    balance += sum;
}

void Account::withdraw(double sum) {
    if (sum <= 0) {
        throw logic_error("can not withdraw negative amount of cash.");
    }
    if (balance - sum < 0) {
        throw logic_error("this account does not have enough money for this transaction.");
    }
    balance -= sum;
}

void Account::chargeFee() {
    balance -= service_fee;
}

void Account::print() const {
    cout << "account number: " << account_number << "; balance: " << balance << endl;
}

void Account::update() {
    this->chargeFee();
}

void SavingsAccount::addInterest() {
    balance *= (1 + interest_rate);
}

double SavingsAccount::getInterestRate() const {
    return interest_rate;
}

SavingsAccount::SavingsAccount(double serviceFee, double interestRate) : Account(serviceFee) {
    this->interest_rate = interestRate;
}

SavingsAccount::SavingsAccount(double interestRate) {
    this->interest_rate = interestRate;
}

void SavingsAccount::print() const {
    cout << "account number: " << account_number << "; balance: " << balance;
    cout << "; interest rate: " << interest_rate << endl;
}

void SavingsAccount::update() {
    Account::update();
    addInterest();
}

CurrentAccount::CurrentAccount(double overdraft) {
    this->overdraft = overdraft;
}

CurrentAccount::CurrentAccount(double serviceFee, double overdraft) : Account(serviceFee) {
    this->overdraft = overdraft;
}

void CurrentAccount::withdraw(double sum) {
    if (sum <= 0) {
        throw logic_error("can not withdraw negative amount of cash.");
    }
    if (balance - sum < -overdraft) {
        throw logic_error("this account does not have enough money for this transaction.");
    }
    balance -= sum;
}

void CurrentAccount::print() const {
    cout << "account number: " << account_number << "; balance: " << balance;
    cout << "; overdraft: " << overdraft << endl;
}

void CurrentAccount::update() {
    Account::update();
    if (balance < 0) {
        cout << "warning: account " << account_number << " has a negative balance." << endl;
    }
}
