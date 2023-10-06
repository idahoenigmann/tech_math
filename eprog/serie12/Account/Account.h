//
// Created by ida on 13.01.21.
//

#ifndef SERIE12_ACCOUNT_H
#define SERIE12_ACCOUNT_H

#include <iostream>
#include <stdexcept>

class Account {
public:
    Account();
    Account(double service_fee);
    ~Account() = default;

    int get_account_number() const;
    double get_service_fee() const;

    void deposit(double sum);
    virtual void withdraw(double sum);
    void chargeFee();
    virtual void print() const;

    virtual void update();

protected:
    int account_number{};
    double balance{};
    double service_fee{};
private:
    static int next_account_number;
};

class SavingsAccount : public Account {
public:
    SavingsAccount(double serviceFee, double interestRate);
    SavingsAccount(double interestRate);

    void addInterest();

    double getInterestRate() const;

    void print() const override;

    void update() override;
protected:
    double interest_rate{};
};

class CurrentAccount : public Account {
public:
    CurrentAccount(double overdraft);
    CurrentAccount(double serviceFee, double overdraft);

    void withdraw(double sum) override;
    void print() const override;

    void update() override;
protected:
    double overdraft{};
};

#endif //SERIE12_ACCOUNT_H
