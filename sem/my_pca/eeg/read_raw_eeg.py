import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne


"""
Information on this file and what to do to get it to run.

Install the package mne. https://mne.tools/stable/index.html

Create a directory named 'data' at the same place you saved this file. Copy all files named 'n*.edf' (where * is one of 
{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16}) and the file 'startend.csv' into the directory 'data'.

Change variable named 'input_number' to the number of recording you would like to process.

Set 'plot_output' to True if you want to visualize the results. One plot is 30s of the data. To run through the entire 
recording quickly set to False.

The code will read the data, apply a low pass and high pass filter, resample the data and select a channel in the 
recording. It then partitions the recording into 30s segments and does a FFT on each segment. The result is saved in a
file named 'n*.csv'.

The resulting csv file is a matrix of dimensions (seconds in recording / 30) times 3000. Each row is a 30s segment. In 
the columns are the amplitudes of the different frequencies, that FFT calculated.
"""

if __name__ == '__main__':
    matplotlib.use('TkAgg')

    plot_output = False      # if True each 30s segment and its corresponding FFT is plotted
    input_number = 16       # recording number, e.g. 1 for reading file n1.csv

    start, end = np.loadtxt("data/startend.csv", delimiter=",", skiprows=1)[input_number - 1, :]
    start, end = int(start) - 1, int(end)

    # read data from edf file
    file = f"data/n{input_number}.edf"
    raw = mne.io.read_raw_edf(file, preload=True)
    raw.filter(0.5, 30)     # low pass and high pass filter
    raw.resample(sfreq=200, npad=0)     # resampling to common frequency

    print(raw.info)

    # check which channels exist
    possible_channels = set(raw.ch_names).intersection({"C4-A1", "C3-A2"})
    # {"Fp2-F4", "FP2-F4", "Fp1-F3", "FP1-F3", "Fp2", "F2-F4", "C4-A1", "F3A2", "C3-A2"})
    channel = possible_channels.pop()
    print(f"channel used: {channel}")

    raw_data = raw.get_data(picks=[channel], return_times=True)

    data = raw_data[0][0, start:end]
    time = raw_data[1][start:end]

    print(f"Duration: {time[-1]}-{time[0]} = {time[-1] - time[0]}s")

    # stop here if you do not want to perform a FFT on the data

    # loop through all 30s segments
    output_data = []
    number_samplepoints = 30 * 200
    sample_spacing = 1.0 / 200.0
    frequencies = np.fft.fftfreq(number_samplepoints, d=sample_spacing)
    frequencies = frequencies[0:len(frequencies) // 2]

    for start in range(0, len(data)//number_samplepoints * number_samplepoints, number_samplepoints):
        # do fft
        fft_output = np.absolute(np.fft.fft(data[start:start + number_samplepoints]))
        amplitude_over_frequency = 2.0 / number_samplepoints * fft_output[0:len(frequencies)]

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
    header = f"amplitudes"
    np.savetxt(f"data/n{input_number}.csv", np.matrix(output_data), delimiter=",", newline="\n", header=header)
