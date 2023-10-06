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

bool check(string roman) {
    int cur{};
    int next{};
    int nextnext{};

    int repetition_freq{};
    int repetition_val{};

    bool five{};

    for (int i{}; i < roman.size(); i++) {
        if (i+2 < roman.size()) {
            cur = value(roman[i]);
            next = value(roman[i+1]);
            nextnext = value(roman[i+2]);
        } else if (i+1 < roman.size()) {
            cur = value(roman[i]);
            next = value(roman[i+1]);
            nextnext = 0;
        } else if (i < roman.size()) {
            cur = value(roman[i]);
            next = 0;
            nextnext = 0;
        }

        if (cur == 5) {
            five = true;
        }

        if (five && next == 1 && nextnext == 5) {
            throw logic_error("invalid: can't add IV(4) to a number ending with 5.");
        }

        if (cur > next) {
            if (cur < nextnext) {
                throw logic_error("invalid: can't have a digit that is smaller than the one after the next digit.");
            }
            //pass;
        } else if (cur == next) {

            if (next < nextnext) {
                throw logic_error("invalid: can't subtract two digits.");
            }
            if (cur == 100 || cur == 10 || cur == 1) {
                //checking for repetition of same char
                if (cur == repetition_val) {
                    repetition_freq++;
                } else {
                    repetition_freq = 1;
                    repetition_val = cur;
                }
                if (repetition_freq >= 3) {
                    throw logic_error("invalid: no repetition of C,X,I more than 3 times.");
                }
            } else if (cur == 500 || cur == 50 || cur == 5) {
                //checking for repetition of same char
                throw logic_error("invalid: no repetition of D,L,V more than once.");
            } else {
                //pass;
            }
        } else {
            if (2*cur == next) {
                throw logic_error ("invalid: can't have a digit followed by the double of it.");
            }

            if (next > nextnext) {
                //pass;
            } else {
                throw logic_error ("invalid: can't have three digits who are bigger than the one before them.");
            }
        }


        if (cur != next && cur == nextnext) {
            if (cur == 1000 || cur == 100 || cur == 10) {
                if (next == 100 || next == 10 || next == 1) {
                    //pass;
                } else {
                    throw logic_error ("invalid: can't have a digit followed by another digit being followed by the first digit. exept the first digit is M, C or X and the second digit is C, X or I. except XCX.");
                }
            } else {
                throw logic_error ("invalid: can't have a digit followed by another digit being followed by the first digit. exept the first digit is M, C or X and the second digit is C, X or I. except XCX.");
            }
        }
    }
    return true;
}



unsigned int roman2dec(string roman) {
    unsigned int res{};
    int cur_val{};
    int next_val{};

    if (check(roman)) {

        for (int i{0}; i<roman.size(); i++) {
            cur_val = value(roman[i]);
            next_val = value(roman[min(i+1, roman.size()-1)]);

            //calculating the decimal value
            if (cur_val >= next_val) {
                res += cur_val;
            } else {
                res += next_val - cur_val;
                i++;
            }
        }
    }
    return res;
}

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

int roman2int(string s) {
    return roman2dec(s);
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