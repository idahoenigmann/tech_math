
def print_a(s1, s2):
    print((s1 + s2)[::-1])


def print_b(s):
    tmp = str.split(s, " ")
    tmp[0], tmp[-1] = tmp[-1], tmp[0]
    return (' '.join(tmp))[::-1]


def print_c():
    for i in range(1, 11):
        print("{:<5} {:<5} {:<5}".format(i, i**2, i**3))


if __name__ == "__main__":
    print_a("Hello ", "World!")

    print(print_b("The house stood on a slight rise just on the edge of the village."))
    print(print_b(print_b("The house stood on a slight rise just on the edge of the village.")))

    print_c()
