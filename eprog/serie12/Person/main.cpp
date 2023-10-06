#include <iostream>

#include "Person.h"

using namespace std;

int main() {
    Person p;
    Student s("Daisy Duck", "Entenhausen", 1234, "Philosophy");
    Employee e("Batman", "some cave", 1000.99, "saving the day");

    p.setName("Donald Duck");
    p.setAddress("Entenhausen");

    cout << s.getName() << endl;
    p.print();
    s.print();
    e.print();

    return 0;
}
