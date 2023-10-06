cmake_minimum_required(VERSION 3.17)
project(serie12)

set(CMAKE_CXX_STANDARD 20)

add_executable(serie12_1 Person/main.cpp Person/Person.cpp Person/Person.h)

add_executable(serie12_2 Account/main.cpp Account/Account.cpp Account/Account.h Account/Bank.cpp Account/Bank.h)

add_executable(serie12_4 ReducedMatrix/ReducedMatrix.cpp ReducedMatrix/ReducedMatrix.h ReducedMatrix/main.cpp)