//
// Created by ida on 02.12.20.
//

#include <iostream>
#include <string>

using std::cout;
using std::cin;
using std::endl;
using std::boolalpha;
using std::string;

bool isPalindrome(string word) {
    for (int i=0; i <= word.length() / 2; i++) {
        if (tolower(word.c_str()[i]) != tolower(word.c_str()[word.length() - i - 1])) {
            return false;
        }
    }
    return true;
}

int main() {
    cout << "Checks whether a word is palindrome." << endl;

    string word;

    cout << "Please enter a word: ";
    cin >> word;

    cout << endl << "Is Palindrome: " << boolalpha << isPalindrome(word) << endl;

    return 0;
}