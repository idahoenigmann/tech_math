//
// Created by ida on 10.12.20.
//

#ifndef SERIE09_123_STOPWATCH_H
#define SERIE09_123_STOPWATCH_H

#include <ctime>
#include <iostream>

class Stopwatch {
public:
    void pushButtonStartStop();
    void pushButtonReset();
    void print();
private:
    clock_t start_time = 0;
    double ellapsed_time = 0;
    bool is_running = false;
};


#endif //SERIE09_123_STOPWATCH_H
