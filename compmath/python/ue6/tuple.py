
def tuple_a(int_tuple):
    return ''.join(str(e) for e in int_tuple)


def tuple_b(int_tuples):
    res = []
    for i in range(0, len(int_tuples[0])):
        res.append(sum(e[i] for e in int_tuples))
    return tuple(res)


def tuple_c(int_tuples):
    return list(sum(int_tuples[j][i] for i in range(0, len(int_tuples[j]))) for j in range(0, len(int_tuples)))


def tuple_d(string):
    return list(string)


if __name__ == '__main__':
    print(tuple_a((1, 2, 3)))
    print(tuple_a((100, 42, 21322314)))

    print(tuple_b(((1, 2, 3), (3, 2, 1))))
    print(tuple_b(((1, 2, 3, 4), (3, 2, 1, 6), (1, 1, 1, 1))))
    # print(tuple_b(((1, 2, 3, 4), (1, 6), (1, 1, 1, 1))))      # error

    print(tuple_c([(1, 2), (2, 3), (3, 4)]))
    print(tuple_c([(1, 2, 3), (2, 3), (3, 4), (10, 42)]))

    print(tuple_d("Hello World!"))
