//
// Created by ida on 09.12.20.
//

#ifndef SERIE09_123_INTVECTOR_H
#define SERIE09_123_INTVECTOR_H

#include <stdexcept>

class IntVector {
public:
    IntVector() = default;
    explicit IntVector(unsigned int length, int value=0);
    explicit IntVector(int number);
    ~IntVector();

    void setCoefficient(unsigned int index, int value);
    int getCoefficient(unsigned int index);
    unsigned int getLength() const;
private:
    unsigned int length=0;
    int* data = nullptr;
};


#endif //SERIE09_123_INTVECTOR_H
