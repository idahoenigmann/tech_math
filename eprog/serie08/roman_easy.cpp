//
// Created by ida on 02.12.20.
//

#include <iostream>
#include <string>
#include <cassert>

#define min(a, b) (a<b?a:b)

using std::cout;
using std::endl;
using std::cin;
using std::string;
using std::logic_error;

string int2roman(int n) {
    string roman;
    assert(1 <= n);
    assert(n <= 3999);

    int numbers[] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    string letters[] = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

    for (int i=0; i < 13; i++) {
        int mod = n / numbers[i];
        for (int j=0; j < mod; j++) {
            roman += letters[i];
        }
        n -= mod * numbers[i];
    }

    return roman;
}

int value(char digit) {
    switch (digit) {
        case 'M':
            return 1000;
        case 'D':
            return 500;
        case 'C':
            return 100;
        case 'L':
            return 50;
        case 'X':
            return 10;
        case 'V':
            return 5;
        case 'I':
            return 1;
        default:
            throw logic_error("invalid roman digit: " + string(1, digit));
    }
}


int roman2int(string roman) {
    int res{0};
    char cur_val{};
    char next_val{};


    for (int i{0}; i<roman.size(); i++) {
        cur_val = roman[i];
        next_val = roman[min(i+1, roman.size()-1)];

        if (value(cur_val) >= value(next_val)) {
            res += value(cur_val);
        } else {
            res += value(next_val)-value(cur_val);
            i++;
        }
    }
    return res;
}


int main() {
    string roman;
    int n;

    cin >> roman;
    cout << roman2int(roman) << endl;

    cin >> n;
    cout << int2roman(n) << endl;

    return 0;
}