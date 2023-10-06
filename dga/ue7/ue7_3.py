import math

def new_bf(E):
    n = len(E)

    # INIT
    d = [math.inf] * n
    d[0] = 0

    for j in range(0, n * n):
        for i in range(0, n-1):
            for u in range(0, n):
                for v in range(0, n):
                    # RELAX
                    if d[v] > d[u] + E[u][v]:
                        d[v] = d[u] + E[u][v]
        for u in range(0, n):
            for v in range(0, n):
                if d[v] > d[u] + E[u][v]:
                    d[v] = -math.inf

    return d

if __name__ == "__main__":
    E = [[0       , 10      , math.inf, math.inf, -7      , math.inf, math.inf, math.inf],
         [math.inf, 0       , 6       , math.inf, math.inf, math.inf, math.inf, math.inf],
         [math.inf, math.inf, 0       , -11     , math.inf, math.inf, 0       , math.inf],
         [math.inf, 3       , math.inf, 0       , math.inf, math.inf, math.inf, math.inf],
         [math.inf, math.inf, math.inf, math.inf, 0       , 3       , math.inf, math.inf],
         [math.inf, math.inf, math.inf, math.inf, math.inf, 0       , 1       , math.inf],
         [math.inf, math.inf, math.inf, math.inf, math.inf, math.inf, 0       , math.inf],
         [8       , math.inf, math.inf, math.inf, math.inf, math.inf, math.inf, 0       ]]

    res = new_bf(E)
    print(res)
