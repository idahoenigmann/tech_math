
def odd_even_a_odd(integer):
    if not isinstance(integer, int):
        raise TypeError(str(integer) + " is not an integer.")
    return sum(int(e) % 2 for e in list(str(abs(integer))))


def odd_even_a_even(integer):
    return int(len(str(integer))) - odd_even_a_odd(integer)


def odd_even_b_odd(num):
    return odd_even_a_odd(int(num * 1e10))


def odd_even_b_even(num):
    return odd_even_a_even(int(num * 1e10))    # 0 is even, right?


def odd_even_c(num):
    return sum(1 if int(e) in (2, 3, 5, 7) else 0 for e in list(str(num)))


if __name__ == "__main__":
    print(odd_even_a_odd(-123497531))
    print(odd_even_a_even(123497531))

    # print(odd_even_a_odd("hello world"))
    # print(odd_even_a_even("hello world"))

    print(odd_even_b_odd(3.1415))
    print(odd_even_b_even(3.1415))

    print(odd_even_c(1234567890))
    print(odd_even_c(146890))
    print(odd_even_c(2357))
    print(odd_even_c(123))
