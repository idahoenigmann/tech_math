//
// Created by ida on 13.01.21.
//

#include "Person.h"

using namespace std;

Person::Person(const string &name, const string &address) : name(name), address(address) {
    this->name = name;
    this->address = address;
}

const std::string &Person::getName() const {
    return name;
}

void Person::setName(const std::string &name) {
    this->name = name;
}

const std::string &Person::getAddress() const {
    return address;
}

void Person::setAddress(const std::string &address) {
    this->address = address;
}

Student::Student(const string &name, const string &address, int studentNumber, const string &study) : Person(name,
                                                                                                             address) {
    this->student_number = studentNumber;
    this->study = study;
}

int Student::getStudentNumber() const {
    return student_number;
}

void Student::setStudentNumber(int studentNumber) {
    student_number = studentNumber;
}

const std::string &Student::getStudy() const {
    return study;
}

void Student::setStudy(const std::string &study) {
    this->study = study;
}

Employee::Employee(const string &name, const string &address, double salary, const string &job) : Person(name, address) {
    this->salary = salary;
    this->job = job;
}

double Employee::getSalary() const {
    return salary;
}

void Employee::setSalary(double salary) {
    this->salary = salary;
}

const std::string &Employee::getJob() const {
    return job;
}

void Employee::setJob(const std::string &job) {
    this->job = job;
}

void Person::print() {
    cout << "Name: " << name << "; Address: " << address << endl;
}

void Student::print() {
    cout << "Name: " << name << "; Address: " << address;
    cout << "; Student number: " << student_number << "; Study: " << study << endl;
}

void Employee::print() {
    cout << "Name: " << name << "; Address: " << address;
    cout << "; Salary: " << salary << "; Job: " << job << endl;
}
