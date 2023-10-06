import collections


def lists_a(int_list):
    return len(set(int_list)) == len(int_list)


def lists_b(input_str):
    return ''.join(sorted(list(input_str), key=lambda e: e.upper()))    # ignores upper/lower case


def lists_c(input_list):
    duplicates = collections.Counter(input_list) - collections.Counter(set(input_list))
    input_list[:] = list(set(input_list))       # setting list elements changes the original list
    return list(duplicates)


def lists_d(input_list, sub_list):
    return not bool(sum(not (e in input_list) for e in sub_list))


def lists_d2(input_list, sub_list):
    for i in range(len(input_list) - len(sub_list)):
        if sub_list == input_list[i:i+len(sub_list)]:
            return True
    return False


def lists_e(input_list, n):
    return list(str(i) + str(j) for j in range(1, n+1) for i in input_list)


if __name__ == "__main__":
    print(lists_a((1, 2, 3, 4)))
    print(lists_a((1, 2, 3, 4, 3, 5)))

    print(lists_b("Hello World!"))

    tmp_lst = [1, 2, 3, 2, 4, 4, 6, 1]
    print(lists_c(tmp_lst))
    print(tmp_lst)

    print(lists_d([1, 2, 3, 4], [2, 5]))
    print(lists_d([1, 2, 3, 4], [2, 3]))

    print(lists_e(['p', 'q'], 5))
