import random


def sequences_a(a0, n):
    a = a0
    for i in range(n):
        if a % 2 == 0:
            a = a / 2
        else:
            a = 3 * a + 1
    return a


def sequences_b():
    for i in range(1000):
        random_num = random.randint(1, 1000)
        res = sequences_a(random_num, 1000)
        if res not in (1, 2, 4):
            print(random_num)


if __name__ == "__main__":
    random_num = random.randint(1, 1000)
    print(random_num)
    print(sequences_a(random_num, 1000))

    sequences_b()
