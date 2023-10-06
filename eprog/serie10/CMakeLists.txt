cmake_minimum_required(VERSION 3.17)
project(serie10)

set(CMAKE_CXX_STANDARD 20)

add_executable(serie10_12 main12.cpp Matrix.cpp)

add_executable(serie10_34 Matrix.cpp main34.cpp)

add_executable(serie10_5 Matrix.cpp main5.cpp)

add_executable(serie10_6 Matrix.cpp vector.cpp main6.cpp)