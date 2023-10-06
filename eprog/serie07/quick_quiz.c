//
// Created by ida on 27.11.20.
//


#include <stdio.h>
#include <assert.h>
#include <math.h>

int quiz(double tau) {
    double a = 2;
    double an = sqrt(2);
    int n = 0;

    assert(tau > 0);

    while(fabs(a - an) / fabs(a) >= tau) {
        an = sqrt(2+an);
        n++;
    }
    return n;
}

void scanPointInSet(double* x, double* y, double* z) {

    while ((*x) * (*y) < 0 || (*z) < 0) {
        printf("Please enter a value for x: ");
        scanf("%lf",x);
        printf("Please enter a value for y: ");
        scanf("%lf",y);
        printf("Please enter a value for z: ");
        scanf("%lf",z);
    }
}

Account* newAccount(char* name, int number, double balance) {
    Account* account = memalloc(sizeof(Account));

    accout->name = memalloc(sizeof(char) * (strlen(name) + 1));

    strcpy(account->name, name);
    account->number = number;
    account->balance = balance;

    return account;
}

Account* delAccount(Account* account) {
    assert(account != NULL);
    assert(account->name != NULL);

    free(account->name);
    free(account);
    return NULL;
}

int main() {


}