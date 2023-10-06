cmake_minimum_required(VERSION 3.17)
project(serie09_123)

set(CMAKE_CXX_STANDARD 20)

add_executable(serie09_123 main.cpp IntVector.cpp Factorization.cpp Fraction.cpp utils.cpp)

add_executable(serie09_8 Stopwatch.cpp stopwatch_main.cpp)
