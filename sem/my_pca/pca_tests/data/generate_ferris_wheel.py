from csv import writer
import numpy as np


if __name__ == '__main__':
    with open('ferris_wheel.csv', 'w') as file:
        csv_writer = writer(file, delimiter=",")
        csv_writer.writerow(["x position", "y position"])
        for angle in range(0, 360, 5):
            x = np.cos(angle / 180 * np.pi) + np.random.random() * 0.15
            y = np.sin(angle / 180 * np.pi) + np.random.random() * 0.05

            csv_writer.writerow([x, y])
