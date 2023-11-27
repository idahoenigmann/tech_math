import matplotlib
import matplotlib.pyplot as plt


def lane_riesenfeld(px, py, n):
    # copy
    x = [e for e in px for _ in range(2)]
    y = [e for e in py for _ in range(2)]

    # average n times
    for _ in range(n):
        x = [(x[i] + x[i + 1]) / 2 for i in range(len(x) - 1)]
        y = [(y[i] + y[i + 1]) / 2 for i in range(len(y) - 1)]

    return x, y


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots()

    px = [0, 0, 3, 7, 7, 6]
    py = [2, 4, 5, 3, 2, 0]

    for i in range(len(px)):
        ax.plot(px[i:i+2], py[i:i+2], c='black', linewidth=3.5)

    colors = ['blue', 'green', 'red']

    for l in range(3):
        px, py = lane_riesenfeld(px, py, 5)

        for i in range(len(px)):
            ax.plot(px[i:i+2], py[i:i+2], c=colors[l], linewidth=3.5)

    plt.show()
