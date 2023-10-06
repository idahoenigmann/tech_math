//
// Created by ida on 09.12.20.
//

#include "IntVector.h"

using namespace std;

IntVector::IntVector(unsigned int length, int value) {
    data = new int[length];
    this->length = length;
    for(int i=0; i < (int)length; i++) {
        data[i] = value;
    }
}

IntVector::~IntVector() {
    delete[] data;
    data = nullptr;
    length = 0;
}

void IntVector::setCoefficient(unsigned int index, int value) {
    if (index >= length) {
        throw logic_error("Index out of bound.");
    }
    data[index] = value;
}

unsigned int IntVector::getLength() const {
    return length;
}

IntVector::IntVector(int number) {
    if (number <= 1) {
        throw logic_error("Sieve of Eratosthenes only works for numbers bigger than 1.");
    }

    int* tmp = new int[number - 1];
    int cnt_removed{0};
    for (int i=0; i < number - 1; i++) {
        tmp[i] = i+2;
    }

    for (int i=0; i < number - 1; i++) {
        if (tmp[i] == -1) {
            continue;
        }
        for (int j=i; j < number - 1; j++) {
            if (tmp[j] == -1) {
                continue;
            }
            if (tmp[j] % tmp[i] == 0 && tmp[j] != tmp[i]) {
                tmp[j] = -1;
                cnt_removed++;
            }
        }
    }

    int idx = 0;
    data = new int[number - 1 - cnt_removed];

    length = number - 1 - cnt_removed;

    for (int i=0; i < number - 1; i++) {
        if (tmp[i] >= 0) {
            data[idx] = tmp[i];
            idx++;
        }
    }

    delete[] tmp;
}

int IntVector::getCoefficient(unsigned int index) {
    if (index >= length) {
        throw logic_error("Index out of bound.");
    }
    return data[index];
}
