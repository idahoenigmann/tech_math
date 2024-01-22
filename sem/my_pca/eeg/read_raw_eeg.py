import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    plot_output = False
    input_number = 1

    start, end = np.loadtxt("data/startend.csv", delimiter=",", skiprows=1)[input_number - 1, :]
    start, end = int(start), int(end)

    # read data from edf file
    file = f"data/n{input_number}.edf"
    raw = mne.io.read_raw_edf(file, preload=True)
    raw = raw.resample(sfreq=200, npad=0)

    print(raw.info)

    # check which channels exist
    possible_channels = set(raw.ch_names).intersection({"F2-F4", "Fp2-F4", "F1-F3", "Fp1-F3"})
    channel = possible_channels.pop()

    raw_data = raw.get_data(picks=[channel], start=int(start*512/200), stop=int(end*512/200), return_times=True)

    data = raw_data[0][0]
    time = raw_data[1]

    print(f"Duration: {time[-1]}-{time[0]} = {time[-1] - time[0]}s")

    # loop through all 30s segments
    output_data = []
    number_samplepoints = 30 * 200
    sample_spacing = 1.0 / 200.0
    frequencies = np.linspace(0.0, 1.0 / (2.0 * sample_spacing), number_samplepoints // 2)

    for start in range(0, len(data)//number_samplepoints * number_samplepoints, number_samplepoints):
        # do fft
        fft_output = np.absolute(np.fft.fft(data[start:start + number_samplepoints]))
        amplitude_over_frequency = 2.0 / number_samplepoints * fft_output[:number_samplepoints // 2]

        # plot figures
        if plot_output:
            fig, axs = plt.subplots(nrows=2)
            axs[0].plot(time[start:start + number_samplepoints], data[start:start + number_samplepoints])
            axs[0].set_xlabel("time (s)")
            axs[0].set_ylabel("amplitude")

            axs[1].plot(frequencies, amplitude_over_frequency)
            axs[1].set_xlabel("frequency (Hz)")
            axs[1].set_ylabel("amplitude")

            plt.show()

        # save result
        output_data.append(amplitude_over_frequency)

    # write output to csv file
    header = ",".join([f"t{i} amplitude" for i in range(amplitude_over_frequency.shape[0])])
    np.savetxt(f"data/n{input_number}.csv", np.matrix(output_data), delimiter=",", newline="\n", header=header)
