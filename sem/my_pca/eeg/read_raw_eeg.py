import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    plot_output = False
    input_number = 2

    start, end = np.loadtxt("data/startend.csv", delimiter=",", skiprows=1)[input_number - 1, :]
    start, end = int(start), int(end)

    # read data from edf file
    file = f"data/n{input_number}.edf"
    raw = mne.io.read_raw_edf(file, preload=True)
    raw = raw.resample(sfreq=200, npad=0)

    print(raw.info)

    # check which channels exist
    possible_channels = set(raw.ch_names).intersection(set(["F2-F4", "Fp2-F4", "F1-F3", "Fp1-F3"]))
    channel = possible_channels.pop()

    raw_data = raw.get_data(picks=[channel], start=int(start*512/200), stop=int(end*512/200), return_times=True)

    data = raw_data[0][0]
    time = raw_data[1]

    print(f"Duration: {time[-1]}-{time[0]} = {time[-1] - time[0]}s")

    # loop through all 30s segments
    output_data = []
    start, end = 0, 0
    idx = 0
    number_samplepoints, sample_spacing = 0, 0
    while end < len(time):
        start = end
        # find end of next 30s segment
        end = next((idx for idx, value in enumerate(time) if value > time[start] + 30), -1)
        if end == -1:
            break

        # save frequencies only once
        if idx == 0:
            number_samplepoints = end - start
            sample_spacing = 1.0 / 200.0
            frequencies = np.linspace(0.0, 1.0 / (2.0 * sample_spacing), number_samplepoints // 2)
            output_data.append(frequencies)

        # do fft
        x = np.linspace(0.0, number_samplepoints * sample_spacing, number_samplepoints)
        y = data[start:end]
        fft_output = np.absolute(np.fft.fft(y))

        # plot figures
        if plot_output:
            fig, axs = plt.subplots(nrows=2)
            axs[0].plot(time[start:end], data[start:end])
            axs[0].set_xlabel("time (s)")
            axs[0].set_ylabel("amplitude")

            axs[1].plot(frequencies, 2.0 / number_samplepoints * fft_output[:number_samplepoints // 2])
            axs[1].set_xlabel("frequency (Hz)")
            axs[1].set_ylabel("amplitude")

            plt.show()

        # save result
        output_data.append(2.0/number_samplepoints*fft_output[:number_samplepoints//2])
        idx += 1

    # write output to csv file
    header = "frequency, " + ",".join([f"t{i} amplitude" for i in range(idx)])
    np.savetxt(f"data/n{input_number}.csv", np.matrix(output_data).T, delimiter=",", newline="\n", header=header)
