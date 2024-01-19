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

    print(f"Duration: {time[-1] - time[0]}s")

    start = 0
    end = 0
    idx = 0
    while end < len(time):
        start = end
        end = next(idx for idx, value in enumerate(time) if value > time[start] + 30)

        number_samplepoints = end - start
        sample_spacing = 1.0/512.0
        x = np.linspace(0.0, number_samplepoints*sample_spacing, number_samplepoints)
        y = data[start:end]
        fft_output = np.absolute(np.fft.fft(y))
        frequncies = np.linspace(0.0, 1.0/(2.0*sample_spacing), number_samplepoints//2)

        # plot figures
        fig, axs = plt.subplots(nrows=2)
        axs[0].plot(time[start:end], data[start:end])
        axs[0].set_xlabel("time (s)")
        axs[0].set_ylabel("amplitude")

        axs[1].plot(frequncies, 2.0/number_samplepoints*fft_output[:number_samplepoints//2])
        axs[1].set_xlabel("frequency (Hz)")
        axs[1].set_ylabel("amplitude")

        output_data = np.matrix([frequncies, 2.0/number_samplepoints*fft_output[:number_samplepoints//2]]).transpose()
        np.savetxt(f"data/n1_{idx}.csv", output_data, delimiter=",", newline="\n")
        plt.show()
        idx += 1
