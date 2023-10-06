

def strings_a(s_in, s_find, s_replace):
    return s_in.replace(s_find, s_replace)


def strings_b(s, capitalize=True):
    return list(e.capitalize() if capitalize else e for e in s.split(" "))


if __name__ == '__main__':
    print(strings_a("asdfjkl", "fjk", "qwerty"))
    print(strings_a("asdfjklasdfjkl", "fjk", " "))

    print(strings_b("Hello World, what a nice day!"))
    print(strings_b("Hello World, what a nice day!", False))
