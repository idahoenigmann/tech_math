import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    input_number = 1

    start, end = np.loadtxt("data/startend.csv", delimiter=",", skiprows=1)[input_number - 1, :]
    start, end = int(start) - 1, int(end)

    # read sleep stages
    sleep_stages_seg = np.loadtxt(f"data/CAPsleepdatan{input_number}.csv", delimiter=";", dtype=int, skiprows=1)
    sleep_stages_seg = sleep_stages_seg[int(start/200/30):int(end/200/30), 0]

    # read data from edf file
    file = f"data/n{input_number}.edf"
    raw = mne.io.read_raw_edf(file, preload=True)
    raw.filter(0.5, 30)
    raw.resample(sfreq=200, npad=0)

    print(raw.info)

    # check which channels exist
    possible_channels = set(raw.ch_names).intersection({"Fp2-F4", "FP2-F4", "Fp1-F3", "FP1-F3", "Fp2",
                                                        "F2-F4", "C4-A1", "F3A2", "C3-A2"})
    channel = possible_channels.pop()
    print(f"channel used: {channel}")

    raw_data = raw.get_data(picks=[channel], return_times=True)

    data = raw_data[0][0, start:end]
    print(data.shape)
    time = raw_data[1][start:end]

    print(f"Duration: {time[-1]}-{time[0]} = {time[-1] - time[0]}s")

    # loop through all 30s segments
    output_data = {1: [], 2: [], 3: [], 4: [], 5: []}
    number_samplepoints = 30 * 200
    total_number_samplepoints = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for idx in range(len(sleep_stages_seg)):
        total_number_samplepoints[sleep_stages_seg[idx]] += number_samplepoints
        output_data[sleep_stages_seg[idx]].append(data[idx * number_samplepoints:idx * number_samplepoints + number_samplepoints])

    sleep_stages_name = ["S3", "S2", "S1", "REM", "awake"]

    for sleep_stage in output_data.keys():
        if len(output_data[sleep_stage]) == 0:
            print(f"skipping sleep stage {sleep_stage}={sleep_stages_name[sleep_stage - 1]} as there is no data in this category.")
            continue
        sleep_stage_data = np.concatenate(output_data[sleep_stage])
        nbr_sample_points = total_number_samplepoints[sleep_stage]
        # do fft
        sample_spacing = 1.0 / 200.0
        frequencies = np.fft.fftfreq(nbr_sample_points, d=sample_spacing)
        frequencies = frequencies[0:len(frequencies) // 2]
        fft_output = np.absolute(np.fft.fft(sleep_stage_data))
        amplitude_over_frequency = 2.0 / nbr_sample_points * fft_output[0:len(frequencies)]

        # plot figures
        fig, axs = plt.subplots(nrows=2)
        fig.suptitle(f"Total data from sleep stage {sleep_stages_name[sleep_stage - 1]}")
        axs[0].plot(time[start:start + nbr_sample_points], sleep_stage_data[0: nbr_sample_points])
        axs[0].set_xlabel("time (s)")
        axs[0].set_ylabel("amplitude")

        axs[1].plot(frequencies, amplitude_over_frequency)
        axs[1].set_xlabel("frequency (Hz)")
        axs[1].set_ylabel("amplitude")

        # fig.canvas.manager.full_screen_toggle()
        plt.show()
