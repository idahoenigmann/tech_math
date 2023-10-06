//
// Created by ida on 13.01.21.
//

#ifndef SERIE12_PERSON_H
#define SERIE12_PERSON_H

#include <iostream>
#include <string>

class Person {
public:
    Person() = default;
    Person(const std::string &name, const std::string &address);
    virtual ~Person() = default;

    const std::string &getName() const;
    void setName(const std::string &name);

    const std::string &getAddress() const;
    void setAddress(const std::string &address);

    virtual void print();

protected:
    std::string name{};
    std::string address{};
};

class Student : public Person {
public:
    Student() = default;
    Student(const std::string &name, const std::string &address, int studentNumber, const std::string &study);
    ~Student() override = default;

    int getStudentNumber() const;
    void setStudentNumber(int studentNumber);

    const std::string &getStudy() const;
    void setStudy(const std::string &study);

    void print() override;

protected:
    int student_number{};
    std::string study{};
};

class Employee : public Person {
public:
    Employee() = default;
    Employee(const std::string &name, const std::string &address, double salary, const std::string &job);
    ~Employee() override = default;

    double getSalary() const;
    void setSalary(double salary);

    const std::string &getJob() const;
    void setJob(const std::string &job);

    void print() override;

protected:
    double salary{};
    std::string job{};
};

#endif //SERIE12_PERSON_H
