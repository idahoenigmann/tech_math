import math

def floyd_warshall(d):
    n = 7

    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                if d[j][i] + d[i][k] < d[j][k]:
                    d[j][k] = d[j][i] + d[i][k]
            if d[j][j] < 0:
                raise Exception

    return d

if __name__ == "__main__":
    d = [[       0,        6,        1,        3, math.inf, math.inf, math.inf],
         [       6,        0,        6, math.inf,        3,        1, math.inf],
         [       1,        6,        0, math.inf, math.inf,        4, math.inf],
         [       3, math.inf, math.inf,        0, math.inf,        1,        8],
         [math.inf,        3, math.inf, math.inf,        0,        5,        2],
         [math.inf,        1,        4,        1,        5,        0,        7],
         [math.inf, math.inf, math.inf,        8,        2,        7,        0]]

    res = floyd_warshall(d)
    for l in res:
        print(l)
