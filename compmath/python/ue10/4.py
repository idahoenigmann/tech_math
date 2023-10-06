
def f(x):
    return 2 * x * x + 4 * x


def f_prime(x):
    return 4 * x + 4


def newton(f, f_prime, x0, tau):
    prev = x0
    x = x0
    fx = 0

    while True:
        prev = x
        x = prev - f(prev) / f_prime(prev)
        fx = f(x)

        if abs(f_prime(x) <= tau):
            return x
        elif abs(x) <= tau:
            if abs(fx) <= tau and abs(x - prev) <= tau:
                return x
        else:
            if abs(fx) <= tau and abs(x - prev) <= tau * abs(x):
                return x


if __name__ == "__main__":
    x0 = input("enter value for x0: ")

    print(newton(f, f_prime, 10, 0.01))
