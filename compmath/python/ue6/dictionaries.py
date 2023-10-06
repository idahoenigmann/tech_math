

def dictionaries_a():
    d = {'key1': [1, 2, {'key2': ['do not get confused', {'tough': [1, 2, [['get me']]]}]}]}

    e = {'key2': [1, [[], {'bug': {'bug': 'get me'}}]]}

    return d['key1'][2]['key2'][1]['tough'][2][0][0], e['key2'][1][1]['bug']['bug']


def dictionaries_b(input_dict):
    return {key[::-1]: val for key, val in input_dict.items()}


if __name__ == "__main__":
    print(dictionaries_a())

    print(dictionaries_b({'key1': 1, 'key2': 'hello world'}))
