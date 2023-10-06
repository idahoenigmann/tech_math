//
// Created by ida on 10.12.20.
//

#include "Stopwatch.h"

using namespace std;

void Stopwatch::pushButtonStartStop() {
    if (is_running) {
        ellapsed_time = (double) (clock() - start_time) / CLOCKS_PER_SEC;
    } else {
        start_time = clock();
    }
    is_running = !is_running;
}

void Stopwatch::pushButtonReset() {
    ellapsed_time = 0;
    is_running = false;
}

void Stopwatch::print() {
    double cpy_ellapsed_time = ellapsed_time;
    int hours = (int)(cpy_ellapsed_time / (60 * 60));
    cpy_ellapsed_time -= hours * 60 * 60;
    int minutes = (int)(cpy_ellapsed_time / 60);
    cpy_ellapsed_time -= minutes * 60;
    int seconds = (int)(cpy_ellapsed_time);
    cpy_ellapsed_time -= seconds;
    int millisec = (int)(cpy_ellapsed_time * 100);
    cout << hours << ":" << minutes << ":" << seconds << "." << millisec << endl;
}
