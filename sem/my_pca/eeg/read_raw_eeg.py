import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    file = "data/n1.edf"
    raw = mne.io.read_raw_edf(file)
    raw_data = raw.get_data(picks=['F2-F4'], start=42001, stop=6918000, return_times=True)

    print(raw.info)
    # raw_data is array of channels followed by array of times
    data = raw_data[0][0]
    time = raw_data[1]
    # raw.plot()

    print(f"Duration: {time[-1]}-{time[0]} = {time[-1] - time[0]}s")

    output_data = []

    start = 0
    end = 0
    idx = 0
    number_samplepoints = 0
    sample_spacing = 0
    while end < len(time):
        start = end
        end = next((idx for idx, value in enumerate(time) if value > time[start] + 30), -1)
        if end == -1:
            break

        if idx == 0:
            number_samplepoints = end - start
            sample_spacing = 1.0 / 512.0
            frequencies = np.linspace(0.0, 1.0 / (2.0 * sample_spacing), number_samplepoints // 2)
            output_data.append(frequencies)

        x = np.linspace(0.0, number_samplepoints * sample_spacing, number_samplepoints)
        y = data[start:end]
        fft_output = np.absolute(np.fft.fft(y))

        # plot figures
        """
        fig, axs = plt.subplots(nrows=2)
        axs[0].plot(time[start:end], data[start:end])
        axs[0].set_xlabel("time (s)")
        axs[0].set_ylabel("amplitude")

        axs[1].plot(frequencies, 2.0 / number_samplepoints * fft_output[:number_samplepoints // 2])
        axs[1].set_xlabel("frequency (Hz)")
        axs[1].set_ylabel("amplitude")
        
        plt.show()
        """

        output_data.append(2.0/number_samplepoints*fft_output[:number_samplepoints//2])
        idx += 1

    header = "frequency, " + ",".join([f"t{i} amplitude" for i in range(idx)])
    np.savetxt(f"data/n1.csv", np.matrix(output_data).T, delimiter=",", newline="\n", header=header)
